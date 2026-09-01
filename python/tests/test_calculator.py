import ast
import json
import math

import pytest

import calculator


def _eval(expr):
    tree = ast.parse(expr, mode="eval")
    return calculator._eval_ast(tree.body)


def _patch_input(monkeypatch, values):
    it = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


# ---------------------------------------------------------------------------
# format_number
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "number,expected",
    [
        (1.0, "1"),
        (-2.0, "-2"),
        (3.14, "3.14"),
        (1 / 3, "0.333333"),
        (0.5, "0.5"),
    ],
)
def test_format_number(number, expected):
    assert calculator.format_number(number) == expected


# ---------------------------------------------------------------------------
# _eval_ast（AST 白名单解析）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "expr,expected",
    [
        ("1 + 2", 3.0),
        ("10 - 4", 6.0),
        ("6 * 7", 42.0),
        ("8 / 2", 4.0),
        ("10 % 3", 1.0),
        ("10 // 3", 3.0),
        ("2 ** 3", 8.0),
        ("2 ** 3 ** 2", 512.0),
        ("10 + 5 * 2", 20.0),
        ("(10 + 5) * 2", 30.0),
        ("-3", -3.0),
        ("+3", 3.0),
        ("pi", math.pi),
        ("e", math.e),
        ("sqrt(9)", 3.0),
        ("abs(-5)", 5.0),
        ("sqrt(9) + 1", 4.0),
        ("sin(pi / 2)", 1.0),
        ("cos(0)", 1.0),
        ("tan(0)", 0.0),
        ("log(100)", 2.0),
        ("ln(e)", 1.0),
    ],
)
def test_eval_ast_valid(expr, expected):
    assert _eval(expr) == pytest.approx(expected)


@pytest.mark.parametrize(
    "expr",
    [
        "1 / 0",
        "1 // 0",
        "1 % 0",
        "0 ** -1",
        "(-1) ** 0.5",
        "sqrt(-1)",
        "log(0)",
        "log(-1)",
        "ln(0)",
        "ln(-1)",
        "foo(1)",
        "open('x')",
        "math.sin(1)",
        "__import__('os')",
        "1j",
        "'abc'",
        "True",
        "x + 1",
        "[1, 2]",
    ],
)
def test_eval_ast_rejects(expr):
    with pytest.raises(calculator._ExpressionError):
        _eval(expr)


# ---------------------------------------------------------------------------
# evaluate_expression（表达式计算入口）
# ---------------------------------------------------------------------------

def test_evaluate_expression_valid():
    result, entry = calculator.evaluate_expression("10 + 5 * 2")
    assert result == 20.0
    assert entry == ("10 + 5 * 2", calculator.EXPR_OPERATOR, None, 20.0)


@pytest.mark.parametrize(
    "expr",
    [
        "1 / 0",
        "1 +",
        "__import__('os')",
        "10 ** 1000000",
    ],
)
def test_evaluate_expression_errors(expr):
    result, entry = calculator.evaluate_expression(expr)
    assert result is None
    assert entry is None


def test_evaluate_expression_deep_recursion():
    expr = "1" + "+1" * 2000
    result, entry = calculator.evaluate_expression(expr)
    assert result is None
    assert entry is None


# ---------------------------------------------------------------------------
# calculate（二元运算）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "num1,num2,op,expected",
    [
        (5.0, 3.0, "+", 8.0),
        (5.0, 3.0, "-", 2.0),
        (5.0, 3.0, "*", 15.0),
        (5.0, 2.0, "/", 2.5),
        (10.0, 3.0, "%", 1.0),
        (10.0, 3.0, "//", 3.0),
        (2.0, 3.0, "**", 8.0),
    ],
)
def test_calculate_valid(monkeypatch, num1, num2, op, expected):
    _patch_input(monkeypatch, [op])
    result, operator = calculator.calculate(num1, num2)
    assert result == pytest.approx(expected)
    assert operator == op


@pytest.mark.parametrize(
    "num1,num2,op",
    [
        (5.0, 0.0, "/"),
        (5.0, 0.0, "%"),
        (5.0, 0.0, "//"),
        (0.0, -1.0, "**"),
        (-1.0, 0.5, "**"),
        (10.0, 1000.0, "**"),
    ],
)
def test_calculate_errors(monkeypatch, num1, num2, op):
    _patch_input(monkeypatch, [op])
    result, operator = calculator.calculate(num1, num2)
    assert result is None
    assert operator is None


def test_calculate_unknown_operator(monkeypatch):
    _patch_input(monkeypatch, ["^"])
    result, operator = calculator.calculate(1.0, 2.0)
    assert result is None
    assert operator is None


def test_calculate_inf_result_rejected(monkeypatch):
    _patch_input(monkeypatch, ["*"])
    result, operator = calculator.calculate(1e308, 1e308)
    assert result is None
    assert operator is None


# ---------------------------------------------------------------------------
# calculate_unary（一元运算）—— 含 P1-1 的 inf/nan 回归用例
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "operator,num,expected",
    [
        ("sqrt", 9.0, 3.0),
        ("abs", -5.0, 5.0),
        ("abs", 5.0, 5.0),
    ],
)
def test_calculate_unary_valid(monkeypatch, operator, num, expected):
    _patch_input(monkeypatch, [operator, str(num)])
    result, op, n = calculator.calculate_unary()
    assert result == pytest.approx(expected)
    assert op == operator
    assert n == num


@pytest.mark.parametrize(
    "operator,num",
    [
        ("sqrt", -1.0),
        ("sqrt", "inf"),
        ("sqrt", "nan"),
        ("abs", "inf"),
        ("abs", "nan"),
    ],
)
def test_calculate_unary_rejects_nonfinite(monkeypatch, operator, num):
    _patch_input(monkeypatch, [operator, str(num)])
    result, op, n = calculator.calculate_unary()
    assert result is None
    assert op is None
    assert n is None


def test_calculate_unary_unknown_operator(monkeypatch):
    _patch_input(monkeypatch, ["foo"])
    result, op, n = calculator.calculate_unary()
    assert result is None
    assert op is None
    assert n is None


# ---------------------------------------------------------------------------
# 历史记录读写
# ---------------------------------------------------------------------------

def test_load_history_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "nope.json")
    assert calculator.load_history() == []


def test_load_history_corrupted(tmp_path, monkeypatch):
    f = tmp_path / "history.json"
    f.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    assert calculator.load_history() == []


def test_load_history_not_list(tmp_path, monkeypatch):
    f = tmp_path / "history.json"
    f.write_text('{"a": 1}', encoding="utf-8")
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    assert calculator.load_history() == []


def test_load_history_valid(tmp_path, monkeypatch):
    f = tmp_path / "history.json"
    f.write_text(json.dumps([[1, "+", 2, 3], [4, "sqrt", None, 2]]), encoding="utf-8")
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    assert calculator.load_history() == [(1, "+", 2, 3), (4, "sqrt", None, 2)]


def test_load_history_skips_invalid_entries(tmp_path, monkeypatch):
    f = tmp_path / "history.json"
    f.write_text(json.dumps([[1, "+", 2, 3], "bad", [1, 2, 3]]), encoding="utf-8")
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    assert calculator.load_history() == [(1, "+", 2, 3)]


def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0), ("1+2", "=", None, 3.0)]
    calculator.save_history(history)
    assert calculator.load_history() == history


def test_save_history_rejects_nonfinite(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    calculator.save_history([(float("nan"), "sqrt", None, float("nan"))])
    assert "保存失败" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# 历史记录管理增强：删除 / 撤销（Undo）
# ---------------------------------------------------------------------------

def test_delete_history_entry_valid(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)]
    _patch_input(monkeypatch, ["2"])
    removed = calculator.delete_history_entry(history)
    assert removed == (4.0, "*", 5.0, 20.0)
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]
    assert "1 + 2 = 3" in capsys.readouterr().out


def test_delete_history_entry_empty(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = []
    removed = calculator.delete_history_entry(history)
    assert removed is None
    assert history == []
    assert "没有历史记录" in capsys.readouterr().out


def test_delete_history_entry_invalid_number(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0)]
    _patch_input(monkeypatch, ["abc"])
    removed = calculator.delete_history_entry(history)
    assert removed is None
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert "有效的编号" in capsys.readouterr().out


@pytest.mark.parametrize("choice", ["0", "-1", "99"])
def test_delete_history_entry_out_of_range(tmp_path, monkeypatch, capsys, choice):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0)]
    _patch_input(monkeypatch, [choice])
    removed = calculator.delete_history_entry(history)
    assert removed is None
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert "编号不存在" in capsys.readouterr().out


def test_undo_history_valid(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)]
    removed = calculator.undo_history(history)
    assert removed == (4.0, "*", 5.0, 20.0)
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]
    assert "1 + 2 = 3" in capsys.readouterr().out


def test_undo_history_empty(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = []
    removed = calculator.undo_history(history)
    assert removed is None
    assert history == []
    assert "没有可撤销" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# 删除 + Undo 联动测试
# ---------------------------------------------------------------------------

LINKAGE_ENTRIES = [
    (1.0, "+", 2.0, 3.0),
    (4.0, "*", 5.0, 20.0),
    (6.0, "-", 1.0, 5.0),
]


def test_delete_then_undo_linkage(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    calculator.save_history(LINKAGE_ENTRIES)
    history = calculator.load_history()
    assert history == LINKAGE_ENTRIES

    _patch_input(monkeypatch, ["2"])
    removed = calculator.delete_history_entry(history)
    assert removed == LINKAGE_ENTRIES[1]
    assert history == [LINKAGE_ENTRIES[0], LINKAGE_ENTRIES[2]]
    assert calculator.load_history() == [LINKAGE_ENTRIES[0], LINKAGE_ENTRIES[2]]

    undone = calculator.undo_history(history)
    assert undone == LINKAGE_ENTRIES[2]
    assert undone != removed
    assert history == [LINKAGE_ENTRIES[0]]
    assert calculator.load_history() == [LINKAGE_ENTRIES[0]]


@pytest.mark.parametrize(
    "delete_index,after_delete,after_undo",
    [
        (1, [LINKAGE_ENTRIES[1], LINKAGE_ENTRIES[2]], [LINKAGE_ENTRIES[1]]),
        (2, [LINKAGE_ENTRIES[0], LINKAGE_ENTRIES[2]], [LINKAGE_ENTRIES[0]]),
        (3, [LINKAGE_ENTRIES[0], LINKAGE_ENTRIES[1]], [LINKAGE_ENTRIES[0]]),
    ],
)
def test_delete_then_undo_positions(tmp_path, monkeypatch, delete_index, after_delete, after_undo):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = list(LINKAGE_ENTRIES)
    calculator.save_history(history)

    _patch_input(monkeypatch, [str(delete_index)])
    calculator.delete_history_entry(history)
    assert history == after_delete
    assert calculator.load_history() == after_delete

    calculator.undo_history(history)
    assert history == after_undo
    assert calculator.load_history() == after_undo


def test_delete_then_undo_empty_boundary(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    calculator.save_history(history)

    _patch_input(monkeypatch, ["1"])
    calculator.delete_history_entry(history)
    assert history == []
    assert calculator.load_history() == []

    undone = calculator.undo_history(history)
    assert undone is None
    assert "没有可撤销" in capsys.readouterr().out
    assert calculator.load_history() == []


def test_delete_then_undo_until_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)]
    calculator.save_history(history)

    _patch_input(monkeypatch, ["1"])
    calculator.delete_history_entry(history)
    assert history == [(4.0, "*", 5.0, 20.0)]

    assert calculator.undo_history(history) == (4.0, "*", 5.0, 20.0)
    assert history == []
    assert calculator.load_history() == []

    assert calculator.undo_history(history) is None
    assert "没有可撤销" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# 第一阶段 CLI：delete_history_entry_at / classify_line / run_command
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "line,expected",
    [
        ("", ("blank", None)),
        ("   ", ("blank", None)),
        ("history", ("command", "history", "")),
        ("  history  ", ("command", "history", "")),
        ("HISTORY", ("command", "history", "")),
        ("delete 3", ("command", "delete", "3")),
        ("  delete   3  ", ("command", "delete", "3")),
        ("undo", ("command", "undo", "")),
        ("clear", ("command", "clear", "")),
        ("help", ("command", "help", "")),
        ("about", ("command", "about", "")),
        ("exit", ("command", "exit", "")),
        ("12 + 5", ("expression", "12 + 5")),
        ("sqrt(144)", ("expression", "sqrt(144)")),
        ("sin(pi / 2)", ("expression", "sin(pi / 2)")),
        ("foo(1)", ("expression", "foo(1)")),
        ("deletexyz", ("expression", "deletexyz")),
        ("pi", ("expression", "pi")),
        ("e", ("expression", "e")),
    ],
)
def test_classify_line(line, expected):
    assert calculator.classify_line(line) == expected


def test_delete_history_entry_at_valid(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)]
    removed = calculator.delete_history_entry_at(history, 2)
    assert removed == (4.0, "*", 5.0, 20.0)
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]
    assert "1 + 2 = 3" in capsys.readouterr().out


def test_delete_history_entry_at_empty(tmp_path, monkeypatch, capsys):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    removed = calculator.delete_history_entry_at([], 1)
    assert removed is None
    assert "没有历史记录" in capsys.readouterr().out


@pytest.mark.parametrize("index", [0, -1, 99])
def test_delete_history_entry_at_out_of_range(tmp_path, monkeypatch, capsys, index):
    f = tmp_path / "history.json"
    monkeypatch.setattr(calculator, "HISTORY_FILE", f)
    history = [(1.0, "+", 2.0, 3.0)]
    removed = calculator.delete_history_entry_at(history, index)
    assert removed is None
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert "编号不存在" in capsys.readouterr().out


def test_run_command_history_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "history", "") == "continue"
    assert "没有历史记录" in capsys.readouterr().out


def test_run_command_history_with_entries(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    assert calculator.run_command(history, "history", "") == "continue"
    assert "1 + 2 = 3" in capsys.readouterr().out


def test_run_command_undo_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "undo", "") == "continue"
    assert "没有可撤销" in capsys.readouterr().out


def test_run_command_undo_valid(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)]
    assert calculator.run_command(history, "undo", "") == "continue"
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]


def test_run_command_delete_valid(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)]
    assert calculator.run_command(history, "delete", "2") == "continue"
    assert history == [(1.0, "+", 2.0, 3.0)]
    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]


def test_run_command_delete_no_arg(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    assert calculator.run_command(history, "delete", "") == "continue"
    assert "delete" in capsys.readouterr().out
    assert history == [(1.0, "+", 2.0, 3.0)]


def test_run_command_delete_non_integer(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    assert calculator.run_command(history, "delete", "abc") == "continue"
    assert "有效的编号" in capsys.readouterr().out
    assert history == [(1.0, "+", 2.0, 3.0)]


def test_run_command_delete_out_of_range(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    assert calculator.run_command(history, "delete", "99") == "continue"
    assert "编号不存在" in capsys.readouterr().out
    assert history == [(1.0, "+", 2.0, 3.0)]


def test_run_command_clear_confirm_yes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    _patch_input(monkeypatch, ["y"])
    assert calculator.run_command(history, "clear", "") == "continue"
    assert history == []
    assert calculator.load_history() == []
    assert "已清空" in capsys.readouterr().out


def test_run_command_clear_confirm_no(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    history = [(1.0, "+", 2.0, 3.0)]
    _patch_input(monkeypatch, ["n"])
    assert calculator.run_command(history, "clear", "") == "continue"
    assert history == [(1.0, "+", 2.0, 3.0)]


def test_run_command_help(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "help", "") == "continue"
    assert "delete" in capsys.readouterr().out


def test_run_command_about(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "about", "") == "continue"
    assert "关于" in capsys.readouterr().out


def test_run_command_exit(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "exit", "") == "exit"


def test_run_command_quit(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "quit", "") == "exit"


def test_run_command_menu(tmp_path, monkeypatch):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    assert calculator.run_command([], "menu", "") == "menu"


def test_classify_line_menu_and_quit():
    assert calculator.classify_line("menu") == ("command", "menu", "")
    assert calculator.classify_line("quit") == ("command", "quit", "")


# ---------------------------------------------------------------------------
# 第二阶段 CLI：handle_expression / run_menu_loop / run_cli
# ---------------------------------------------------------------------------

def _reset_stats(monkeypatch):
    monkeypatch.setattr(calculator, "calculation_count", 0)
    monkeypatch.setattr(calculator, "error_count", 0)


def test_handle_expression_valid(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _reset_stats(monkeypatch)
    history = []

    calculator.handle_expression(history, "12 + 5")

    assert history == [("12 + 5", calculator.EXPR_OPERATOR, None, 17.0)]
    assert calculator.calculation_count == 1
    assert calculator.error_count == 0
    assert calculator.load_history() == [("12 + 5", "=", None, 17.0)]
    assert "结果: 17" in capsys.readouterr().out


def test_handle_expression_invalid(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _reset_stats(monkeypatch)
    history = []

    calculator.handle_expression(history, "1 / 0")

    assert history == []
    assert calculator.calculation_count == 0
    assert calculator.error_count == 1
    assert calculator.load_history() == []
    assert "错误" in capsys.readouterr().out


def test_run_cli_expression(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["12 + 5", "exit"])

    calculator.run_cli()

    out = capsys.readouterr().out
    assert "结果: 17" in out
    assert "总共进行了 1 次计算" in out
    assert calculator.load_history() == [("12 + 5", "=", None, 17.0)]


def test_run_cli_history(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    calculator.save_history([(1.0, "+", 2.0, 3.0)])
    _patch_input(monkeypatch, ["history", "exit"])

    calculator.run_cli()

    assert "1 + 2 = 3" in capsys.readouterr().out


def test_run_cli_undo(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    calculator.save_history([(1.0, "+", 2.0, 3.0)])
    _patch_input(monkeypatch, ["undo", "exit"])

    calculator.run_cli()

    assert calculator.load_history() == []
    assert "已撤销" in capsys.readouterr().out


def test_run_cli_delete(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    calculator.save_history([(1.0, "+", 2.0, 3.0), (4.0, "*", 5.0, 20.0)])
    _patch_input(monkeypatch, ["delete 2", "exit"])

    calculator.run_cli()

    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]
    assert "已删除" in capsys.readouterr().out


def test_run_cli_clear(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    calculator.save_history([(1.0, "+", 2.0, 3.0)])
    _patch_input(monkeypatch, ["clear", "y", "exit"])

    calculator.run_cli()

    assert calculator.load_history() == []
    assert "已清空" in capsys.readouterr().out


def test_run_cli_help(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["help", "exit"])

    calculator.run_cli()

    out = capsys.readouterr().out
    assert "可用命令" in out
    assert "history" in out


def test_run_cli_about(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["about", "exit"])

    calculator.run_cli()

    assert "关于" in capsys.readouterr().out


@pytest.mark.parametrize("command", ["exit", "quit"])
def test_run_cli_exit_quit(tmp_path, monkeypatch, capsys, command):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, [command])

    calculator.run_cli()

    out = capsys.readouterr().out
    assert "感谢使用简单计算器" in out
    assert "总共进行了 0 次计算" in out


def test_run_cli_blank_line(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["", "   ", "exit"])

    calculator.run_cli()

    assert "总共进行了 0 次计算" in capsys.readouterr().out


def test_run_cli_eof(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    monkeypatch.setattr(
        "builtins.input", lambda prompt="": (_ for _ in ()).throw(EOFError)
    )

    calculator.run_cli()

    assert "感谢使用简单计算器" in capsys.readouterr().out


def test_run_menu_loop_exit(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["9"])

    calculator.run_menu_loop([])

    assert "请选择操作" in capsys.readouterr().out


def test_run_cli_menu_returns_to_repl(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["menu", "9", "12 + 5", "exit"])

    calculator.run_cli()

    out = capsys.readouterr().out
    assert "请选择操作" in out
    assert "结果: 17" in out
    assert "总共进行了 1 次计算" in out
    assert calculator.load_history() == [("12 + 5", "=", None, 17.0)]


def test_run_cli_keyboard_interrupt(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    monkeypatch.setattr(
        "builtins.input", lambda prompt="": (_ for _ in ()).throw(KeyboardInterrupt)
    )

    calculator.run_cli()

    assert "感谢使用简单计算器" in capsys.readouterr().out


def test_run_cli_clear_cancel(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    calculator.save_history([(1.0, "+", 2.0, 3.0)])
    _patch_input(monkeypatch, ["clear", "n", "exit"])

    calculator.run_cli()

    assert calculator.load_history() == [(1.0, "+", 2.0, 3.0)]
    assert "已清空" not in capsys.readouterr().out


def test_run_cli_menu_calculation_count_continuity(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _patch_input(monkeypatch, ["menu", "1", "3", "4", "+", "9", "5 + 5", "exit"])

    calculator.run_cli()

    out = capsys.readouterr().out
    assert "总共进行了 2 次计算" in out
    assert calculator.load_history() == [
        (3.0, "+", 4.0, 7.0),
        ("5 + 5", "=", None, 10.0),
    ]


def test_run_cli_menu_error_count_continuity(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(calculator, "HISTORY_FILE", tmp_path / "history.json")
    _reset_stats(monkeypatch)
    _patch_input(monkeypatch, ["menu", "1", "1", "0", "/", "9", "1 / 0", "exit"])

    calculator.run_cli()

    out = capsys.readouterr().out
    assert "总共进行了 0 次计算" in out
    assert calculator.error_count == 2
    assert calculator.calculation_count == 0
    assert calculator.load_history() == []
