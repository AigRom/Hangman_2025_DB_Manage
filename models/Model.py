from models.Database import Database


class Model:
    def __init__(self):
        self.db = Database()

    def add_word(self, word, category):
        self.db.add_word(word, category)

    def update_word(self, word_id, new_word, new_category):
        """Uuendab valitud sõna andmebaasis"""
        self.db.edit_word(word_id, new_word, new_category)  # Kontrolli, et Database.py sisaldaks edit_word() meetodit


    def delete_word(self, word):
        self.db.delete_word(word)

    def get_words(self):
        return self.db.get_all_words()

    def validate_database(self):
        """Kontrollib, kas andmebaasis on words tabel ja õiged veerud"""
        return self.db.validate_database()

    def create_default_database(self):
        """Loob vaikimisi andmebaasi, kui valitud andmebaas on vigane"""
        self.db = Database(db_path="hangman_2025.db")

    def get_unique_categories(self):
        """Tagastab andmebaasis olevad unikaalsed kategooriad"""
        return self.db.get_unique_categories()

    def get_words_by_category(self, category):
        """Tagastab valitud kategooria sõnad või kõik sõnad, kui kategooria on tühi."""
        return self.db.get_words_by_category(category)

    def open_database(self):
        self.db.open_database()

    def close_database(self):
        self.db.close()