from tkinter import *
from tkinter import messagebox

# TODO: po kliknięciu równa się żeby ostatnie działanie dawało ???
# TODO: i żeby można było pobierać działania z historii


class TooLongExpressionException(Exception):
    pass


class Calculator(object):

    def __init__(self):
        self.background_colour = "white"
        self.font_colour = "black"

        self.window = Tk()
        self.window.geometry("465x395")
        self.window.resizable(0, 0)
        self.window.title("Kalkulator")

        self.expression = ""
        self.previous_expression = ""
        self.equation = ""
        self.checkbox_value = BooleanVar()
        self.checkbox_value.set(False)
        self.is_first_character = True
        self.history = []
        self.history_length = 0
        self.is_history_showed = False
        self.is_last_button_equality = False

        self.checkbox = Checkbutton(text="Bright/\nDark mode", font=("Helvetica", 8), variable=self.checkbox_value)  # ogarnąć czemu się nie zaznacza
        self.window_setup()
        mainloop()

    def window_setup(self):
        self.window["bg"] = self.background_colour

        self.entry_box = Text(width=21, height=2, spacing1=10, font=("Helvetica", 30), state="disabled",
                              bg=self.background_colour, fg=self.font_colour)
        self.entry_box.grid(row=0, rowspan=2, column=0, columnspan=5, sticky=W)

        self.make_button("1", 2, 0, lambda x="1": self.character_button_click(x))
        self.make_button("2", 2, 1, lambda x="2": self.character_button_click(x))
        self.make_button("3", 2, 2, lambda x="3": self.character_button_click(x))
        self.make_button("D", 2, 3, self.delete_button_click)
        self.make_button("C", 2, 4, self.clear_button_click)

        self.make_button("4", 3, 0, lambda x="4": self.character_button_click(x))
        self.make_button("5", 3, 1, lambda x="5": self.character_button_click(x))
        self.make_button("6", 3, 2, lambda x="6": self.character_button_click(x))
        self.make_button("+", 3, 3, lambda x="+": self.character_button_click(x))
        self.make_button("-", 3, 4, lambda x="-": self.character_button_click(x))

        self.make_button("7", 4, 0, lambda x="7": self.character_button_click(x))
        self.make_button("8", 4, 1, lambda x="8": self.character_button_click(x))
        self.make_button("9", 4, 2, lambda x="9": self.character_button_click(x))
        self.make_button("*", 4, 3, lambda x="*": self.character_button_click(x))
        self.make_button("/", 4, 4, lambda x="/": self.character_button_click(x))

        self.make_button(".", 5, 0, lambda x=".": self.character_button_click(x))
        self.make_button("0", 5, 1, lambda x="0": self.character_button_click(x))
        self.make_button("=", 5, 2, self.equation_button_click)
        self.make_button("(", 5, 3, lambda x="(": self.character_button_click(x))
        self.make_button(")", 5, 4, lambda x=")": self.character_button_click(x))

        self.button_clearHistory = Button(width=9, height=2, bg=self.background_colour, fg=self.font_colour,
                                          text="History\nclear", font=("Helvetica", 12), command=self.clear_history)
        self.button_clearHistory.grid(row=6, column=3, sticky=W)
        self.button_showHistory = Button(width=9, height=2, bg=self.background_colour, fg=self.font_colour,
                                         text="Show/Hide \nhistory", font=("Helvetica", 12), command=self.show_history)
        self.button_showHistory.grid(row=6, column=4, sticky=W)

        self.checkbox["bg"] = self.background_colour
        self.checkbox["fg"] = self.font_colour
        self.checkbox["command"] = self.style_change
        self.checkbox.grid(row=6, column=0, sticky=W)

        self.label1 = Label(text="Operations history: ", font=("Helvetica", 16),
                            bg=self.background_colour, fg=self.font_colour)
        self.label1.grid(row=0, column=6, sticky=W)

        self.history_listbox = Listbox(width=20, height=8, bg=self.background_colour,
                                       fg=self.font_colour, font=("Helvetica", 20))
        self.history_listbox.grid(row=1, rowspan=5, column=6, columnspan=5, sticky=W)

        self.history_scroll = Scale(length=270, sliderlength=50, showvalue=0)
        self.history_scroll.grid(row=1, rowspan=5, column=11, columnspan=5, sticky=W)
        self.history_scroll.config(command=self.history_listbox.yview)

    def make_button(self, button_text, button_row, button_column, button_action):
        button = Button(width=5, height=1, bg=self.background_colour, fg=self.font_colour,
                        text=button_text, font=("Helvetica", 20), command=button_action)
        button.grid(row=button_row, column=button_column, sticky=W)
        # return button_action  # to raczej nie jest potrzebne

    def character_button_click(self, text):  # po kliknięciu = a potem znaku np * można dalej dodawać litery powyżej 20 znaków
        try:
            if len(self.expression) == 20:
                raise TooLongExpressionException
            if self.is_first_character and str(self.equation) != "" and "+-*/".__contains__(text):
                self.expression += str(self.equation)
                self.is_first_character = False
            else:
                self.is_first_character = False
            self.expression += text
            self.modify_entry_box(self.expression)
            self.is_last_button_equality = False
        except TooLongExpressionException:
            message_box = messagebox.showwarning("Błąd", "Twoje równanie jest za długie!")

    def equation_button_click(self):
        try:
            self.equation = eval(self.expression)
            if str(self.equation) == "()":
                raise SyntaxError

            self.previous_expression = self.expression
            self.modify_entry_box(self.previous_expression)

            equation_to_history = self.expression + "=" + str(self.equation)
            self.add_to_history(equation_to_history)

            self.entry_box["state"] = "normal"
            self.entry_box.insert("end", "\n" + str(self.equation))
            self.entry_box["state"] = "disabled"
        except SyntaxError:
            self.equation_error_message_box("Źle podane równanie, lub jego brak.")
        except ZeroDivisionError:
            self.equation_error_message_box("Dzielenie przez zero nie jest dozwolone.")
        else:
            self.is_last_button_equality = True
            self.is_first_character = True
        finally:
            self.expression = ""

    def delete_button_click(self):
        self.expression = self.expression[:-1]
        self.modify_entry_box(self.expression)

    def clear_button_click(self):
        self.expression = ""
        self.equation = ""
        self.modify_entry_box(self.expression)

    def modify_entry_box(self, text):
        self.entry_box["state"] = "normal"
        self.entry_box.delete(0.0, "end")
        self.entry_box.insert("end", text)
        self.entry_box["state"] = "disabled"

    def equation_error_message_box(self, message):
        self.entry_box["state"] = "normal"
        self.entry_box.delete(0.0, "end")
        self.entry_box["state"] = "disabled"
        message_box = messagebox.showerror("Błąd", message)

    def style_change(self):  # ogarnąć czemu się nie zaznacza
        if self.checkbox_value.get():
            self.background_colour = "#36393e"  # tryb ciemny
            self.font_colour = "white"
        else:
            self.background_colour = "white"  # tryb jasny
            self.font_colour = "black"

        entry_box_copy = self.entry_box.get(0.0, "end")
        self.window_setup()
        self.modify_entry_box(entry_box_copy)
        self.history_adding()

    def add_to_history(self, text):
        self.history.append(text)
        self.history_listbox.insert(self.history_length, text)
        self.history_length += 1

    def history_adding(self):
        self.history_length = len(self.history)
        for i in range(len(self.history)):
            self.history_listbox.insert(self.history_length, self.history[i])

    def clear_history(self):
        self.history = []
        entry_box_copy = self.entry_box.get(0.0, "end")
        self.window_setup()
        self.modify_entry_box(entry_box_copy)

    def show_history(self):
        self.is_history_showed = not self.is_history_showed
        if self.is_history_showed:
            self.window.geometry("800x395")
        else:
            self.window.geometry("465x395")


def main():
    Calc = Calculator()


main()
