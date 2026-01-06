class Book:
    """Class representing a book with title, author, and ISBN."""
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return f"Title: {self.title} | Author: {self.author} | ISBN: {self.isbn}"

class Library:
    """Class representing a library containing a collection of books."""
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added: '{book.title}'")

    def remove_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Removed: '{book.title}' (ISBN: {isbn})")
                return True
        print(f"Error: Book with ISBN {isbn} not found.")
        return False

    def list_all_books(self):
        print("\n--- Current Library Collection ---")
        if not self.books:
            print("The library is empty.")
        else:
            for book in self.books:
                print(book.display_info())
        print("----------------------------------\n")

    def search_by_title(self, title):
        print(f"Searching for title: '{title}'...")
        results = [book for book in self.books if title.lower() in book.title.lower()]
        if results:
            for book in results:
                print(f"Found: {book.display_info()}")
        else:
            print("No matching books found.")

def main():
    my_library = Library()

    book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    book2 = Book("1984", "George Orwell", "9780451524935")
    book3 = Book("The Hobbit", "J.R.R. Tolkien", "9780547928227")

    my_library.add_book(book1)
    my_library.add_book(book2)
    my_library.add_book(book3)

    my_library.list_all_books()

    my_library.search_by_title("1984")

    my_library.remove_book("9780743273565")
    my_library.list_all_books()

if __name__ == "__main__":
    main()