import io
import os
import sys
import tkinter as tk
from contextlib import redirect_stdout
from pathlib import Path
from tkinter import messagebox, ttk

import calculator

VERSION = "1.2"
AUTHOR = "dyy"

OPERATORS = {"+", "-", "*", "/", "%", "//", "**"}

COLOR_BG = "#EEF0F3"
COLOR_DISPLAY = "#FFFFFF"
COLOR_DIGIT_BG = "#FFFFFF"
COLOR_DIGIT_FG = "#111827"
COLOR_OPERATOR_BG = "#E2E8F0"
COLOR_OPERATOR_FG = "#0F172A"
COLOR_EQUALS_BG = "#4F46E5"
COLOR_EQUALS_FG = "#FFFFFF"
COLOR_DANGER_BG = "#FEE2E2"
COLOR_DANGER_FG = "#B91C1C"
COLOR_UTILITY_BG = "#E5E7EB"
COLOR_UTILITY_FG = "#374151"
COLOR_MUTED = "#6B7280"
COLOR_ERROR = "#DC2626"

FONT_DISPLAY = ("Segoe UI Semibold", 34)
FONT_SUB = ("Segoe UI", 11)
FONT_KEY = ("Segoe UI", 18)
FONT_FUNCTION = ("Segoe UI", 11)
FONT_SECONDARY = ("Segoe UI", 11)

STYLES = {
    "digit": "Digit.TButton",
    "operator": "Operator.TButton",
    "equals": "Equals.TButton",
    "danger": "Danger.TButton",
    "utility": "Utility.TButton",
    "function": "Function.TButton",
}


def _configure_history_path():
    if getattr(sys, "frozen", False):
        base = Path(os.environ.get("APPDATA", str(Path.home())))
        directory = base / "calculator"
        directory.mkdir(parents=True, exist_ok=True)
        calculator.HISTORY_FILE = directory / "history.json"


def format_history_entry(num1, operator, num2, result):
    if operator == calculator.EXPR_OPERATOR:
        return f"{num1} = {calculator.format_number(result)}"
    if num2 is None:
        return f"{operator}({calculator.format_number(num1)}) = {calculator.format_number(result)}"
    return f"{calculator.format_number(num1)} {operator} {calculator.format_number(num2)} = {calculator.format_number(result)}"


def compute_insert(text, result_shown, token):
    if result_shown and token not in OPERATORS:
        text = ""
    return text + token


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        _configure_history_path()
        self.title(f"计算器 {VERSION}")
        self.resizable(False, False)
        self.geometry("380x560")
        self.configure(bg=COLOR_BG)

        self._history_win = None
        self._history_listbox = None
        self._result_shown = False

        self.history, _ = self._call(calculator.load_history)

        self.expression_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.expression_var.trace_add("write", self._on_expression_changed)

        self._setup_style()
        self._build_display()
        self._build_buttons()
        self._build_functions()
        self._build_bottom()
        self._bind_keys()

        self.display.focus_set()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=COLOR_BG)

        style.configure(
            "TEntry",
            fieldbackground=COLOR_DISPLAY,
            foreground=COLOR_DIGIT_FG,
            borderwidth=0,
            relief="flat",
            font=FONT_DISPLAY,
            insertcolor=COLOR_DIGIT_FG,
        )

        style.configure(
            "Digit.TButton",
            background=COLOR_DIGIT_BG,
            foreground=COLOR_DIGIT_FG,
            font=FONT_KEY,
            relief="flat",
            borderwidth=0,
            padding=(0, 12),
        )
        style.map(
            "Digit.TButton",
            background=[("active", "#E5E7EB"), ("pressed", "#D1D5DB")],
        )

        style.configure(
            "Operator.TButton",
            background=COLOR_OPERATOR_BG,
            foreground=COLOR_OPERATOR_FG,
            font=FONT_KEY,
            relief="flat",
            borderwidth=0,
            padding=(0, 12),
        )
        style.map(
            "Operator.TButton",
            background=[("active", "#CBD5E1"), ("pressed", "#94A3B8")],
        )

        style.configure(
            "Equals.TButton",
            background=COLOR_EQUALS_BG,
            foreground=COLOR_EQUALS_FG,
            font=FONT_KEY,
            relief="flat",
            borderwidth=0,
            padding=(0, 12),
        )
        style.map(
            "Equals.TButton",
            background=[("active", "#4338CA"), ("pressed", "#3730A3")],
        )

        style.configure(
            "Danger.TButton",
            background=COLOR_DANGER_BG,
            foreground=COLOR_DANGER_FG,
            font=FONT_KEY,
            relief="flat",
            borderwidth=0,
            padding=(0, 12),
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#FECACA"), ("pressed", "#FCA5A5")],
        )

        style.configure(
            "Utility.TButton",
            background=COLOR_UTILITY_BG,
            foreground=COLOR_UTILITY_FG,
            font=FONT_KEY,
            relief="flat",
            borderwidth=0,
            padding=(0, 12),
        )
        style.map(
            "Utility.TButton",
            background=[("active", "#D1D5DB"), ("pressed", "#9CA3AF")],
        )

        style.configure(
            "Function.TButton",
            background=COLOR_UTILITY_BG,
            foreground=COLOR_UTILITY_FG,
            font=FONT_FUNCTION,
            relief="flat",
            borderwidth=0,
            padding=(0, 8),
        )
        style.map(
            "Function.TButton",
            background=[("active", "#D1D5DB"), ("pressed", "#9CA3AF")],
        )

        style.configure(
            "Secondary.TButton",
            background=COLOR_BG,
            foreground=COLOR_MUTED,
            font=FONT_SECONDARY,
            relief="flat",
            borderwidth=0,
            padding=(10, 6),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#E2E8F0"), ("pressed", "#D1D5DB")],
            foreground=[("active", COLOR_DIGIT_FG)],
        )

    def _build_display(self):
        card = tk.Frame(self, bg=COLOR_DISPLAY)
        card.pack(fill="x", padx=14, pady=(14, 0))

        self.sub_display = tk.Label(
            card,
            textvariable=self.status_var,
            anchor="e",
            bg=COLOR_DISPLAY,
            fg=COLOR_MUTED,
            font=FONT_SUB,
        )
        self.sub_display.pack(fill="x", padx=14, pady=(12, 0))

        self.display = ttk.Entry(card, textvariable=self.expression_var, justify="right")
        self.display.pack(fill="x", padx=14, pady=(2, 14))

    def _button_rows(self):
        return [
            [("C", "clear", "", 1, "danger"), ("⌫", "backspace", "", 1, "utility"),
             ("(", "token", "(", 1, "digit"), (")", "token", ")", 1, "digit"),
             ("÷", "token", "/", 1, "operator")],
            [("7", "token", "7", 1, "digit"), ("8", "token", "8", 1, "digit"),
             ("9", "token", "9", 1, "digit"), ("π", "token", "pi", 1, "digit"),
             ("×", "token", "*", 1, "operator")],
            [("4", "token", "4", 1, "digit"), ("5", "token", "5", 1, "digit"),
             ("6", "token", "6", 1, "digit"), ("e", "token", "e", 1, "digit"),
             ("−", "token", "-", 1, "operator")],
            [("1", "token", "1", 1, "digit"), ("2", "token", "2", 1, "digit"),
             ("3", "token", "3", 1, "digit"), ("%", "token", "%", 1, "operator"),
             ("+", "token", "+", 1, "operator")],
            [("0", "token", "0", 2, "digit"), (".", "token", ".", 1, "digit"),
             ("^", "token", "**", 1, "operator"), ("=", "equals", "", 1, "equals")],
        ]

    def _function_row(self):
        return [
            ("√", "token", "sqrt(", "function"),
            ("abs", "token", "abs(", "function"),
            ("sin", "token", "sin(", "function"),
            ("cos", "token", "cos(", "function"),
            ("tan", "token", "tan(", "function"),
            ("log", "token", "log(", "function"),
            ("ln", "token", "ln(", "function"),
            ("//", "token", "//", "function"),
        ]

    def _build_buttons(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=14, pady=(10, 4))

        for r, row in enumerate(self._button_rows()):
            frame.rowconfigure(r, weight=1)
            col = 0
            for label, action, token, span, style_key in row:
                button = ttk.Button(
                    frame,
                    text=label,
                    style=STYLES[style_key],
                    command=lambda a=action, t=token: self._on_button(a, t),
                )
                button.grid(row=r, column=col, columnspan=span, sticky="nsew", padx=3, pady=3)
                col += span

        for c in range(5):
            frame.columnconfigure(c, weight=1)

    def _build_functions(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=14, pady=(0, 4))

        for c, (label, action, token, style_key) in enumerate(self._function_row()):
            button = ttk.Button(
                frame,
                text=label,
                style=STYLES[style_key],
                command=lambda a=action, t=token: self._on_button(a, t),
            )
            button.grid(row=0, column=c, sticky="nsew", padx=3, pady=3)
            frame.columnconfigure(c, weight=1)

    def _build_bottom(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=14, pady=(4, 14))
        ttk.Button(frame, text="历史记录", style="Secondary.TButton",
                   command=self.open_history).pack(side="left")
        ttk.Button(frame, text="关于", style="Secondary.TButton",
                   command=self.show_about).pack(side="left", padx=(8, 0))

    def _bind_keys(self):
        self.display.bind("<Return>", lambda e: self.evaluate())
        self.display.bind("<Escape>", lambda e: self.clear())

    @staticmethod
    def _call(func, *args, **kwargs):
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = func(*args, **kwargs)
        return result, buf.getvalue()

    @staticmethod
    def _extract_error(output):
        message = output.strip()
        prefix = "错误:"
        if message.startswith(prefix):
            message = message[len(prefix):].strip()
        return message or "表达式错误"

    def _set_sub(self, text, color=COLOR_MUTED):
        self.status_var.set(text)
        self.sub_display.config(fg=color)

    def _on_button(self, action, token):
        if action == "token":
            self.insert_token(token)
        elif action == "clear":
            self.clear()
        elif action == "backspace":
            self.backspace()
        elif action == "equals":
            self.evaluate()

    def insert_token(self, token):
        self.expression_var.set(
            compute_insert(self.expression_var.get(), self._result_shown, token)
        )
        self._set_sub("")
        self.display.focus_set()
        self.display.icursor(tk.END)

    def _on_expression_changed(self, *args):
        self._result_shown = False

    def backspace(self):
        current = self.expression_var.get()
        self.expression_var.set(current[:-1])
        self._set_sub("")
        self._result_shown = False
        self.display.focus_set()
        self.display.icursor(tk.END)

    def clear(self):
        self.expression_var.set("")
        self._set_sub("")
        self._result_shown = False
        self.display.focus_set()

    def evaluate(self):
        expr = self.expression_var.get().strip()
        if not expr:
            return

        (result, entry), output = self._call(calculator.evaluate_expression, expr)

        if result is None:
            self._set_sub("错误: " + self._extract_error(output), COLOR_ERROR)
            self._result_shown = False
            return

        self.expression_var.set(calculator.format_number(result))
        self._set_sub(f"{expr} = {calculator.format_number(result)}")
        self._result_shown = True
        self.history.append(entry)
        self._call(calculator.save_history, self.history)
        self._refresh_open_history()

    def open_history(self):
        if self._history_win is not None and self._history_win.winfo_exists():
            self._refresh_history_listbox()
            self._history_win.lift()
            return

        win = tk.Toplevel(self)
        win.title("历史记录")
        win.transient(self)

        list_frame = ttk.Frame(win)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15, width=48)
        scrollbar.config(command=listbox.yview)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(btn_frame, text="删除选中", command=self._delete_selected).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="撤销", command=self._undo).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="清空", command=self._clear_history).pack(side="left", padx=2)

        def _on_close():
            self._history_win = None
            self._history_listbox = None
            win.destroy()

        ttk.Button(btn_frame, text="关闭", command=_on_close).pack(side="right", padx=2)
        win.protocol("WM_DELETE_WINDOW", _on_close)

        self._history_win = win
        self._history_listbox = listbox
        self._refresh_history_listbox()

    def _refresh_history_listbox(self):
        if self._history_listbox is None:
            return
        self._history_listbox.delete(0, tk.END)
        for entry in self.history:
            self._history_listbox.insert(tk.END, format_history_entry(*entry))

    def _refresh_open_history(self):
        if self._history_win is not None and self._history_win.winfo_exists():
            self._refresh_history_listbox()

    def _delete_selected(self):
        listbox = self._history_listbox
        if listbox is None:
            return
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("历史记录", "请先选择一条记录。", parent=self._history_win)
            return
        index = selection[0]
        if 0 <= index < len(self.history):
            del self.history[index]
            self._call(calculator.save_history, self.history)
            self._refresh_history_listbox()

    def _undo(self):
        if not self.history:
            messagebox.showinfo("历史记录", "没有可撤销的历史记录。", parent=self._history_win)
            return
        self.history.pop()
        self._call(calculator.save_history, self.history)
        self._refresh_history_listbox()

    def _clear_history(self):
        if not self.history:
            messagebox.showinfo("历史记录", "没有历史记录。", parent=self._history_win)
            return
        if messagebox.askyesno("清空历史", "是否清空历史记录？", parent=self._history_win):
            self.history.clear()
            self._call(calculator.save_history, self.history)
            self._refresh_history_listbox()

    def show_about(self):
        messagebox.showinfo(
            "关于",
            f"简单计算器\n版本 {VERSION}\n作者: {AUTHOR}\n一个用于学习 Python 的简单计算器项目",
            parent=self,
        )


def main():
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
