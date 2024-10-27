# First, install required packages:
# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error
import os

class LibraryManagementSystem:
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='library_management',
                user='Ayush',     # Replace with your MySQL username
                password='ayush123'  # Replace with your MySQL password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Successfully connected to MySQL database!")
                return True
        except Error as e:
            print(f"Error: {e}")
            return False
            
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")
            
    def add_book(self):
        """Add a new book to the library"""
        print("\n=== Add New Book ===")
        try:
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            isbn = input("Enter ISBN: ")
            copies = int(input("Enter number of copies: "))
            
            query = """INSERT INTO Library (title, author, isbn, status, copies_available) 
                      VALUES (%s, %s, %s, 'Available', %s)"""
            values = (title, author, isbn, copies)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Book added successfully!")
            
        except Error as e:
            print(f"Error: {e}")
            
    def delete_book(self):
        """Delete a book from the library"""
        print("\n=== Delete Book ===")
        try:
            book_id = input("Enter book ID to delete: ")
            
            # First check if book exists
            self.cursor.execute("SELECT title FROM Library WHERE book_id = %s", (book_id,))
            book = self.cursor.fetchone()
            
            if book:
                confirm = input(f"Are you sure you want to delete '{book[0]}'? (y/n): ")
                if confirm.lower() == 'y':
                    self.cursor.execute("DELETE FROM Library WHERE book_id = %s", (book_id,))
                    self.connection.commit()
                    print("Book deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Book not found!")
                
        except Error as e:
            print(f"Error: {e}")
            
    def edit_book(self):
        """Edit book details"""
        print("\n=== Edit Book ===")
        try:
            book_id = input("Enter book ID to edit: ")
            
            # Check if book exists
            self.cursor.execute("SELECT * FROM Library WHERE book_id = %s", (book_id,))
            book = self.cursor.fetchone()
            
            if book:
                print(f"\nCurrent details:")
                print(f"1. Title: {book[1]}")
                print(f"2. Author: {book[2]}")
                print(f"3. ISBN: {book[3]}")
                print(f"4. Copies available: {book[5]}")
                
                field = input("\nEnter number of field to edit (1-4): ")
                new_value = input("Enter new value: ")
                
                if field == '1':
                    query = "UPDATE Library SET title = %s WHERE book_id = %s"
                elif field == '2':
                    query = "UPDATE Library SET author = %s WHERE book_id = %s"
                elif field == '3':
                    query = "UPDATE Library SET isbn = %s WHERE book_id = %s"
                elif field == '4':
                    query = "UPDATE Library SET copies_available = %s WHERE book_id = %s"
                else:
                    print("Invalid field number!")
                    return
                
                self.cursor.execute(query, (new_value, book_id))
                self.connection.commit()
                print("Book updated successfully!")
            else:
                print("Book not found!")
                
        except Error as e:
            print(f"Error: {e}")
            
    def display_books(self):
        """Display all books"""
        print("\n=== Library Books ===")
        try:
            self.cursor.execute("SELECT * FROM Library")
            books = self.cursor.fetchall()
            
            if books:
                print("\nID | Title | Author | ISBN | Status | Copies")
                print("-" * 60)
                for book in books:
                    print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]}")
            else:
                print("No books found in the library.")
                
        except Error as e:
            print(f"Error: {e}")
            
    def main_menu(self):
        """Display and handle main menu"""
        while True:
            print("\n=== Library Management System ===")
            print("1. Add Book")
            print("2. Delete Book")
            print("3. Edit Book")
            print("4. Display Books")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.delete_book()
            elif choice == '3':
                self.edit_book()
            elif choice == '4':
                self.display_books()
            elif choice == '5':
                print("Thank you for using Library Management System!")
                self.disconnect()
                break
            else:
                print("Invalid choice! Please try again.")

# Main program
if __name__ == "__main__":
    library = LibraryManagementSystem()
    if library.connect():
        library.main_menu()