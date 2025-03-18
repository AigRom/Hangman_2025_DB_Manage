import sqlite3
import os
from tkinter.filedialog import askopenfilename

class Database:
    def __init__(self, db_path="databases/hangman_2025.db"):
        """Klass andmebaasi haldamiseks"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None

        # Kontrollime, kas kaust "databases" eksisteerib, kui ei, siis loome selle
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        self.connect()

    def connect(self):
        """Ühendub andmebaasiga, kui pole olemas, siis loob selle."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print("Andmebaasi viga:", e)

    def create_table(self):
        """Loob andmebaasi tabeli, kui seda pole olemas."""
        query = """
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            category TEXT NOT NULL
        )"""
        self.cursor.execute(query)
        self.conn.commit()

    def open_database(self):
        """Avab kasutaja valitud andmebaasi ja ühendub sellega."""
        file_path = askopenfilename(filetypes=[("SQLite Database", "*.db")])
        if file_path:
            self.close()  # Sulgeb vana ühenduse enne uue avamist
            self.db_path = file_path
            self.connect()
            return True
        return False

    def add_word(self, word, category):
        """Lisab sõna andmebaasi."""
        query = "INSERT INTO words (word, category) VALUES (?, ?)"
        self.cursor.execute(query, (word, category))
        self.conn.commit()

    def update_word(self, word_id, word, category):
        """Uuendab sõna andmebaasis."""
        query = "UPDATE words SET word = ?, category = ? WHERE id = ?"
        self.cursor.execute(query, (word, category, word_id))
        self.conn.commit()

    def delete_word(self, word_id):
        """Kustutab sõna."""
        query = "DELETE FROM words WHERE id = ?"
        self.cursor.execute(query, (word_id,))
        self.conn.commit()

    def get_all_words(self):
        """Võtab kõik sõnad ja tagastab listina."""
        self.cursor.execute("SELECT id, word, category FROM words")
        return self.cursor.fetchall()

    def edit_word(self, word_id, new_word, new_category):
        """Uuendab sõna ja kategooriat ID alusel."""
        self.cursor.execute("UPDATE words SET word = ?, category = ? WHERE id = ?", (new_word, new_category, word_id))
        self.conn.commit()

    def get_unique_categories(self):
        """Tagastab kõik unikaalsed kategooriad"""
        self.cursor.execute("SELECT DISTINCT category FROM words")
        return [row[0] for row in self.cursor.fetchall()]

    def get_words_by_category(self, category):
        """Võtab valitud kategooria sõnad või kõik sõnad, kui kategooria on tühi."""
        if category == "Vali kategooria":
            self.cursor.execute("SELECT id, word, category FROM words")
        else:
            self.cursor.execute("SELECT id, word, category FROM words WHERE category = ?", (category,))
        return self.cursor.fetchall()

    def validate_database(self):
        """Kontrollib, kas andmebaas sisaldab õiget words tabelit ja õigeid veerge"""
        try:
            self.cursor.execute("PRAGMA table_info(words)")
            columns = [row[1] for row in self.cursor.fetchall()]
            return set(columns) == {"id", "word", "category"}
        except sqlite3.Error:
            return False

    def close(self):
        """Sulgeb andmebaasiühenduse, kui see on avatud."""
        if self.conn:
            self.conn.close()
            self.conn = None


