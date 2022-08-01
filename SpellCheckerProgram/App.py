import tkinter as tk
import re

master = tk.Tk()


class App(tk.Frame):
    def __init__(self, corpus, spell_checker, bigram_model):
        # Initializing our Corpus object
        self.dictionary = corpus
        self.spell_checker = spell_checker
        self.bigram_model = bigram_model
        self.unigram = bigram_model.create_unigram()  # unique words
        model, unigram_count, bigram_count = bigram_model.create_bigram(corpus.get_file_data())
        self.probabilities = bigram_model.bigram_probability_calculation(model=model, unigram_count=unigram_count,
                                                                    bigram_count=bigram_count)
        self.last_word_position = "1.0"
        self.non_word_error_count = 0
        self.real_word_error_count = 0
        self.candidate_words = []

        tk.Frame.__init__(self)
        self.pack()

        # title of the application
        self.master.title('Spell Checker Program')

        # Main Frame
        self.mainframe = tk.Frame(self.master, width=1200, height=800)
        self.mainframe.pack()

        # Search field query value
        self.search_query = tk.StringVar()

        # Menu Bar
        self.menu_bar = tk.Menu(master)
        self.menu_bar.add_command(label='Settings', command=self.settings)
        self.menu_bar.add_command(label='Clear', command=self.clear)
        self.master.config(menu=self.menu_bar)

        # Right Menu
        self.popup_menu = tk.Menu(self, tearoff=0)

        # Left Part of the window
        self.text_frame = tk.Frame(self.mainframe, width=600, height=300)
        self.text_frame.pack(side='left')

        # Text area and binding listener
        self.entry = tk.Text(self.text_frame, borderwidth=1, cursor='dot', bg='#d2d4c8')
        self.entry.pack(side='top')
        self.entry.focus()
        self.entry.bind('<FocusIn>', func=self.remove_placeholder)
        self.entry.bind('<FocusOut>', func=self.add_placeholder)
        self.entry.bind('<space>', func=self.space_pressed)
        self.entry.bind('<Return>', func=self.enter_pressed)
        self.entry.bind('<BackSpace>', func=self.backspace_pressed)
        self.entry.bind('<Key>', func=self.key_pressed)
        self.entry.bind('<Button-3>', func=self.mouse_right_click_menu)
        self.entry.bind('<KeyRelease>', func=self.limit_check)

        # Error Label
        self.error_label = tk.Label(self.text_frame, text='')
        self.error_label.pack(side='bottom')

        # Adding placeholder to the text area
        self.add_placeholder()

        # Right part of window
        self.right_frame = tk.Frame(self.mainframe)
        self.right_frame.pack(side='right', expand=1, fill=tk.Y)

        # List box with dictionary
        self.list_label = tk.Label(self.right_frame, text='Dictionary')
        self.list_label.pack(side='top')

        self.listbox = tk.Listbox(self.right_frame, cursor='spider')
        self.listbox.pack(side='top')

        self.listbox.bind('<Double-Button-1>', func=self.dictionary_double_click)

        # populate dictionary with data
        self.populate_list()

        # Search Box Area
        self.search_box = tk.Frame(self.right_frame)
        self.search_box.pack(side='bottom')

        # Search Box Label
        self.search_label = tk.Label(self.search_box, text='Search')
        self.search_label.pack(side='left')

        # Search Field
        self.search_field = tk.Entry(self.search_box, textvariable=self.search_query)
        self.search_field.pack(side='right')

        # Search field bind listener
        self.search_field.focus()
        self.search_field.bind('<KeyRelease>', self.search)

    # Clears Text area
    def clear(self):
        self.entry.delete("1.0", tk.END)

    # TODO Later we can add some basic setting to our app
    def settings(self):
        self.clear_list()
        self.populate_list()

    # Removes placeholder on focus text area
    def remove_placeholder(self, *args):
        placeholder = self.entry.get("1.0", tk.END)
        if placeholder.strip() == "Text Editor (500 words)":
            self.entry.delete("1.0", tk.END)

    # Adds placeholder on focus out text area
    def add_placeholder(self, *args):
        placeholder = self.entry.get("1.0", tk.END)
        if len(placeholder.strip()) == 0:
            self.entry.insert(tk.INSERT, "Text Editor (500 words)")

    def populate_list(self):
        """Populates List box with unique words from corpus"""
        for item in self.dictionary.get_dictionary():
            self.listbox.insert(tk.END, item)

    # Clears List box
    def clear_list(self):
        self.listbox.delete(0, tk.END)

    # Check limit of 500 words
    def limit_check(self, *args):
        datas = self.entry.get("1.0", tk.END)
        datas = self.tokenizer(datas)

        if len(datas) > 500:
            print("limit is reached: ", len(datas))
            position_indexes = self.entry.index(tk.INSERT).split(".")
            self.entry.delete(f"{position_indexes[0]}.{int(position_indexes[1]) - len(datas[-1])}", tk.END)

    # Right Click Menu
    def mouse_right_click_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def dictionary_double_click(self, event):
        selected_text = self.listbox.selection_get()
        self.entry.insert(tk.INSERT, selected_text)

    # update label and last word position on backspace button click
    def backspace_pressed(self, *args):
        if self.entry.tag_ranges("sel"):
            self.last_word_position = self.entry.index("sel.first")
            self._update_error_label()
        else:
            position_indexes = self.entry.index(tk.INSERT).split(".")

            if int(position_indexes[1]) > 0:
                self.last_word_position = f"{position_indexes[0]}.{int(position_indexes[1]) - 1}"
            elif int(position_indexes[0]) > 1:
                self.last_word_position = f"{int(position_indexes[0]) - 1}.{int(position_indexes[1])}"
            else:
                self.last_word_position = "1.0"
                self._reset_error_label()

    def enter_pressed(self, *args):
        self.check_error()
        position_indexes = self.last_word_position.split(".")
        self.last_word_position = f"{int(position_indexes[0]) + 1}.0"

    def space_pressed(self, *args):
        self.check_error()

    def key_pressed(self, event):
        if event.char == ".":
            self.check_error()
        elif event.char == ",":
            self.check_error()
        elif event.char == "?":
            self.check_error()
        elif event.char == "!":
            self.check_error()

    # TODO Later we will add functionality to check spelling on typing
    def check_error(self):
        # sentence = self.entry.get(self.last_word_position, tk.END)
        # variable sentence returns the previous word
        sentence = self.entry.get("1.0", tk.END).split(" ")[len(self.entry.get("1.0", tk.END).split(" ")) - 1]
        last_position = self.entry.index(tk.INSERT).split(".")
        position_indexes = self.last_word_position.split(".")
        self.last_word_position = f"{position_indexes[0]}.{int(last_position[1]) - len(sentence)}"

        # tokenize previous word
        words = self.tokenizer(sentence)
        for word in words:
            data = self.entry.get("1.0", tk.END)
            data = self.tokenizer(data)
            color = ''
            underline = False
            error_type = ''
            if word not in self.unigram:
                color = 'red'
                underline = True
                error_type = 'non_word_error'
            elif len(data) > 1 and self.bigram_model.check_word_error(self.probabilities, data, word):
                color = 'yellow'
                underline = True
                error_type = 'real_word_error'

            if underline:
                self.entry.tag_add(
                    word,
                    self.last_word_position,
                    f"{position_indexes[0]}.{int(position_indexes[1]) + len(word)}")
                self.entry.tag_bind(
                    word,
                    '<Button-3>',
                    lambda event, arg1=error_type, arg2=word: self._pop(event, arg1, arg2))

                position_indexes = self._mark_error(
                    word,
                    self.last_word_position,
                    color=color,
                    underline=underline,
                    error_type=error_type
                )

        self.last_word_position = f"{position_indexes[0]}.{int(position_indexes[1]) + len(sentence)}"

    def _pop(self, event, error_type, word):
        """calls _populate_context_menu() function with candidates generated
        from _candidate_words_calculation() function"""
        candidates = self._candidate_words_calculation(error_type, word)

        self._populate_context_menu(candidates)

    def _mark_error(self, error, position, color, underline, error_type):
        if error_type == 'non_word_error':
            self.non_word_error_count += 1
        elif error_type == 'real_word_error':
            self.real_word_error_count += 1

        position = self.entry.search(error, position, tk.END)  # Search for error word position
        position_indexes = position.split(".")  # Spit position into row and column
        self.entry.tag_add(
            f"{error_type}_{self.non_word_error_count}",
            f"{position}",
            f"{position_indexes[0]}.{int(position_indexes[1]) + len(error)}"
        )

        self.entry.tag_config(
            f"{error_type}_{self.non_word_error_count}",
            foreground=color, underline=underline
        )  # background="red",

        self.error_label['text'] = f"Error count (non real word / real word): " \
                                   f"{self.non_word_error_count} / {self.real_word_error_count}"

        return position_indexes

    def _candidate_words_calculation(self, error_type, word):
        """generate a list of sorted candidates"""
        data = self.entry.get("1.0", tk.END)
        data = self.tokenizer(data)
        if len(data) > 1:
            if error_type == 'non_word_error':
                return self.spell_checker.get_candidates(word)
            elif error_type == 'real_word_error':
                return self.bigram_model.check_word_error(self.probabilities, data, word)
        return []

    # Right Click Menu
    def _populate_context_menu(self, candidate_words):
        """create a list of option in menu limit by 15 options"""
        self.popup_menu.add_command(label="Candidate (MED)")
        self.popup_menu.add_separator()
        self.popup_menu.delete(2, tk.END)  # delete old populated data

        if len(candidate_words) == 0:  # Check if nothing to suggest then pop information nothing to suggest
            self.popup_menu.add_command(label="Nothing to suggest")

        counter = 0
        for error_type, error_word, correction, probability, med in candidate_words:
            if counter > 20:
                break
            self.popup_menu.add_command(  # Populate context menu with suggestions and add event to be able to replace
                label=f"{correction} ({med})",
                command=lambda arg1=correction: self.select_text(arg1)
            )
            counter += 1  # Update counter to have less then 15 words to suggest

    # Select all
    def select_text(self, selection_word):
        """select text by using mouse click"""
        if self.entry.tag_ranges("sel"):
            start_index = self.entry.index("sel.first")
            end_index = self.entry.index("sel.last")
            self.entry.delete(start_index, end_index)
            self.entry.insert(start_index, selection_word)
            self._update_error_label()

    def _count_errors(self):
        """display error count"""
        sentence = self.entry.get("1.0", tk.END)
        words = self.tokenizer(sentence)
        non_word_counter = 0
        real_word_counter = 0
        for word in words:
            if word not in self.unigram:
                non_word_counter += 1
            elif len(words) > 2 and self.bigram_model.check_word_error(self.probabilities, words, word):
                real_word_counter += 1
        return non_word_counter, real_word_counter

    def _update_error_label(self):
        non_error_count, real_word_error_count = self._count_errors()
        self.non_word_error_count -= non_error_count
        self.real_word_error_count -= real_word_error_count
        self.error_label['text'] = f"Error count (non real word / real word): " \
                                   f"{self.non_word_error_count} / {self.real_word_error_count}"

    def _reset_error_label(self):
        self.non_word_error_count = 0
        self.real_word_error_count = 0
        self.error_label['text'] = f"Error count (non real word / real word): " \
                                   f"{self.non_word_error_count} / {self.real_word_error_count}"

    # Search word from dictionary
    def search(self, *args):
        """search word from dictionary"""
        query = self.search_query.get()

        self.clear_list()
        if len(query.strip()) > 0:
            for item in self.dictionary.get_dictionary():
                if query in item:
                    self.listbox.insert(tk.END, item)
        else:
            self.populate_list()

    def tokenizer(self, input_text):
        """convert the text to lower case"""
        return re.findall(r'[^0-9\s]\w+', input_text.lower())

