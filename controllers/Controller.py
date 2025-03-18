from tkinter import END, messagebox


class Controller:
    def __init__(self, model, view):
        """
        Kontrolleri konstruktor
        :param model: main-is loodud mudel
        :param view:  main-is loodud view
        """
        self.model = model
        self.view = view

        # Rippmenüü funktsionaalsus
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.combobox_change)
        self.view.get_btn_add.config(command=self.add_word)
        self.view.get_btn_edit.config(command=self.edit_word)
        self.view.get_btn_delete.config(command=self.delete_word)
        self.view.get_my_table.bind("<Double-1>", self.select_word)
        self.view.get_btn_open.config(command=self.open_database)
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.filter_by_category)

        self.populate_table()

    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        # print(self.view.get_combo_categories.get(), end=" => ") # Tekst rippmenüüst => Hoonaed
        # print(self.view.get_combo_categories.current()) # Rippmenüü index => 1
        if self.view.get_combo_categories.current() > 0:  # Vali kategooria on 0
            self.view.get_txt_category.delete(0, END) # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')  # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()

    def populate_table(self):
        """Täidab tabeli ja uuendab kategooriate loetelu."""
        self.view.get_my_table.delete(*self.view.get_my_table.get_children())
        words = self.model.get_words()

        # Uuendame tabeli andmeid
        for i, row in enumerate(words, start=1):
            self.view.get_my_table.insert('', 'end', values=(i, *row))

        # Värskendame kategooriate rippmenüüd
        categories = self.model.get_unique_categories()
        self.view.update_category_list(categories)

    def add_word(self):
        """Lisab sõna andmebaasi."""
        word = self.view.get_txt_word.get()
        category = self.view.get_txt_category.get() if self.view.get_combo_categories.current() == 0 else self.view.get_combo_categories.get()
        if word and category:
            self.model.add_word(word, category)
            self.populate_table()
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_category.delete(0, END)

    def select_word(self, event):
        """Valib tabelist sõna ja täidab vormi andmetega."""
        selected_item = self.view.get_my_table.selection()
        if selected_item:
            values = self.view.get_my_table.item(selected_item, "values")
            self.view.get_txt_word.delete(0, END)
            self.view.get_txt_word.insert(0, values[2])
            self.view.get_txt_category.delete(0, END)
            self.view.get_txt_category.insert(0, values[3])

    def edit_word(self):
        """Muudab valitud sõna."""
        selected_item = self.view.get_my_table.selection()
        if selected_item:
            word_id = self.view.get_my_table.item(selected_item, "values")[1]
            new_word = self.view.get_txt_word.get()
            new_category = self.view.get_txt_category.get()
            self.model.update_word(word_id, new_word, new_category)
            self.populate_table()

    def delete_word(self):
        """Kustutab valitud sõna."""
        selected_item = self.view.get_my_table.selection()
        if selected_item:
            word_id = self.view.get_my_table.item(selected_item, "values")[1]
            self.model.delete_word(word_id)
            self.populate_table()

    def open_database(self):
        """Avab kasutaja valitud andmebaasi ja kontrollib selle struktuuri"""
        if self.model.open_database():
            if not self.model.validate_database():
                messagebox.showwarning("Vigane andmebaas", "Valitud andmebaas ei sisalda õiget tabelit või veerge!\n"
                                                           "Luuakse uus andmebaas 'hangman_2025.db'.")
                self.model.create_default_database()
            self.populate_table()

    def filter_by_category(self, event=None):
        """Filtreerib tabeli valitud kategooria põhjal."""
        selected_category = self.view.get_combo_categories.get()
        words = self.model.get_words_by_category(selected_category)

        # Kustutame vana sisu ja lisame uue vastavalt kategooriale
        self.view.get_my_table.delete(*self.view.get_my_table.get_children())
        for i, row in enumerate(words, start=1):
            self.view.get_my_table.insert('', 'end', values=(i, *row))
