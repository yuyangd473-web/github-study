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
    app._result_shown = False
    app.history = []


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
