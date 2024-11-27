import json
import os

class Library:
    def __init__(self, database_file="library.json"):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            with open(self.database_file, 'w') as db:
                json.dump({"books": [], "borrowed": {}}, db)

    def load_data(self):
        """Load library data from the database file."""
        with open(self.database_file, 'r') as db:
            return json.load(db)

    def save_data(self, data):
        """Save library data to the database file."""
        with open(self.database_file, 'w') as db:
            json.dump(data, db, indent=4)

    def add_book(self, title, author, copies):
        """Add a new book to the library."""
        data = self.load_data()
        books = data["books"]

        for book in books:
            if book["title"].lower() == title.lower() and book["author"].lower() == author.lower():
                book["copies"] += copies
                self.save_data(data)
                return f"Updated '{title}' by {author}. Total copies: {book['copies']}."

        new_book = {"title": title, "author": author, "copies": copies}
        books.append(new_book)
        self.save_data(data)
        return f"Added '{title}' by {author} with {copies} copies."

    def borrow_book(self, member, title):
        """Borrow a book from the library."""
        data = self.load_data()
        books = data["books"]
        borrowed = data["borrowed"]

        for book in books:
            if book["title"].lower() == title.lower() and book["copies"] > 0:
                book["copies"] -= 1
                borrowed.setdefault(member, []).append(title)
                self.save_data(data)
                return f"'{title}' has been borrowed by {member}."

        return f"'{title}' is not available or out of stock."

    def return_book(self, member, title):
        """Return a borrowed book."""
        data = self.load_data()
        books = data["books"]
        borrowed = data["borrowed"]

        if member not in borrowed or title not in borrowed[member]:
            return f"{member} did not borrow '{title}'."

        for book in books:
            if book["title"].lower() == title.lower():
                book["copies"] += 1
                borrowed[member].remove(title)
                if not borrowed[member]:
                    del borrowed[member]
                self.save_data(data)
                return f"'{title}' has been returned by {member}."

        return f"'{title}' not found in the library database."

    def view_books(self):
        """List all books in the library."""
        data = self.load_data()
        books = data["books"]
        if not books:
            return "No books available in the library."
        return "\n".join([f"{book['title']} by {book['author']} - {book['copies']} copies" for book in books])