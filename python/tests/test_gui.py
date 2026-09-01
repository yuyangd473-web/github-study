import tempfile
from pathlib import Path

import pytest

import gui


def test_format_history_expression():
    assert gui.format_history_entry("12+8", "=", None, 20.0) == "12+8 = 20"


def test_format_history_unary():
    assert gui.format_history_entry(-99.0, "abs", None, 99.0) == "abs(-99) = 99"


def test_format_history_binary():
    assert gui.format_history_entry(12.0, "+", 8.0, 20.0) == "12 + 8 = 20"


def test_compute_insert_after_result_digit_starts_new():
    assert gui.compute_insert("22", True, "7") == "7"


def test_compute_insert_after_result_operator_chains():
    assert gui.compute_insert("22", True, "+") == "22+"


def test_compute_insert_after_result_dot_starts_new():
    assert gui.compute_insert("22", True, ".") == "."


def test_compute_insert_normal_appends():
    assert gui.compute_insert("12", False, "+") == "12+"


@pytest.fixture(scope="session")
def app():
    try:
        import tkinter as tk
        probe = tk.Tk()
        probe.destroy()
    except tk.TclError:
        pytest.skip("no display available")

    tmp = tempfile.TemporaryDirectory()
    original = gui.calculator.HISTORY_FILE
    gui.calculator.HISTORY_FILE = Path(tmp.name) / "history.json"
    application = gui.CalculatorApp()
    yield application
    application.destroy()
    gui.calculator.HISTORY_FILE = original
    tmp.cleanup()


@pytest.fixture
def reset(app):
    app.expression_var.set("")
    app.status_var.set("")
    app.easter_var.set("")
    app._result_shown = False
    app.history = []
    gui.calculator.calculation_count = 0
    gui.calculator.error_count = 0


def test_result_then_typing_then_button_keeps_input(app, reset):
    app.expression_var.set("2")
    app.evaluate()
    assert app._result_shown is True
    app.expression_var.set("23")
    assert app._result_shown is False
    app.insert_token("4")
    assert app.expression_var.get() == "234"


def test_result_then_typing_expression_then_enter(app, reset):
    app.expression_var.set("2")
    app.evaluate()
    app.expression_var.set("2+3")
    app.evaluate()
    assert app.expression_var.get() == "5"


def test_result_then_digit_button_starts_new(app, reset):
    app.expression_var.set("2")
    app.evaluate()
    app.insert_token("7")
    assert app.expression_var.get() == "7"


def test_clear_after_result(app, reset):
    app.expression_var.set("2")
    app.evaluate()
    app.clear()
    assert app.expression_var.get() == ""
    assert app._result_shown is False
    app.insert_token("9")
    assert app.expression_var.get() == "9"


def test_backspace_after_result(app, reset):
    app.expression_var.set("123")
    app.evaluate()
    app.backspace()
    assert app.expression_var.get() == "12"
    assert app._result_shown is False


# ---------------------------------------------------------------------------
# GUI 彩蛋与计数（共享 record_result）
# ---------------------------------------------------------------------------

def test_gui_easter_egg_42(app, reset):
    app.expression_var.set("6*7")
    app.evaluate()
    assert "生命" in app.easter_var.get()


def test_gui_easter_egg_114514(app, reset):
    app.expression_var.set("114514")
    app.evaluate()
    assert "1919810" in app.easter_var.get()


def test_gui_easter_egg_1919810(app, reset):
    app.expression_var.set("1919810")
    app.evaluate()
    assert "114514" in app.easter_var.get()


def test_gui_success_increments_count(app, reset):
    app.expression_var.set("2+3")
    app.evaluate()
    assert gui.calculator.calculation_count == 1
    assert gui.calculator.error_count == 0


def test_gui_error_egg_after_three_errors(app, reset):
    for _ in range(3):
        app.expression_var.set("1/0")
        app.evaluate()
    assert gui.calculator.error_count == 3
    assert "连续错误 3 次" in app.easter_var.get()


# ---------------------------------------------------------------------------
# GUI ° 按钮
# ---------------------------------------------------------------------------

def test_degree_button_exists(app):
    tokens = [token for _, _, token, _ in app._function_row()]
    assert "°" in tokens


def test_degree_button_inserts_degree(app, reset):
    app._on_button("token", "°")
    assert "°" in app.expression_var.get()


def test_gui_computes_sin_degrees(app, reset):
    app.expression_var.set("sin(30°)")
    app.evaluate()
    assert app.expression_var.get() == "0.5"


# ---------------------------------------------------------------------------
# GUI 关于入口与作者信息
# ---------------------------------------------------------------------------

def _iter_widgets(widget):
    yield widget
    for child in widget.winfo_children():
        yield from _iter_widgets(child)


def test_about_entry_exists(app):
    labels = [
        w.cget("text")
        for w in _iter_widgets(app)
        if w.winfo_class() == "TButton"
    ]
    assert "关于" in labels


def test_about_entry_triggers_show_about(app):
    buttons = [
        w for w in _iter_widgets(app)
        if w.winfo_class() == "TButton" and w.cget("text") == "关于"
    ]
    assert buttons
    assert buttons[0].cget("command")


def test_show_about_contains_author(app, monkeypatch):
    captured = {}

    def fake_showinfo(title, message, parent=None):
        captured["title"] = title
        captured["message"] = message

    monkeypatch.setattr(gui.messagebox, "showinfo", fake_showinfo)
    app.show_about()
    assert captured["title"] == "关于"
    assert gui.AUTHOR in captured["message"]
    assert gui.VERSION in captured["message"]
