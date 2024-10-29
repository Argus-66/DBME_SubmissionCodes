import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="Ayush",
                password="ayush123",
                database="Assignment8"
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database!")
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error: {e}")
            exit(1)

    def add_record(self):
        try:
            name = input("Enter name: ")
            age = input("Enter age: ")
            email = input("Enter email: ")
            
            query = "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)"
            values = (name, age, email)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Record added successfully!")
        except Error as e:
            print(f"Error adding record: {e}")

    def view_records(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            records = self.cursor.fetchall()
            
            if not records:
                print("No records found.")
                return
                
            print("\nAll Records:")
            print("ID\tName\tAge\tEmail")
            print("-" * 50)
            for record in records:
                print(f"{record[0]}\t{record[1]}\t{record[2]}\t{record[3]}")
        except Error as e:
            print(f"Error viewing records: {e}")

    def edit_record(self):
        try:
            record_id = input("Enter the ID of the record to edit: ")
            
            # Check if record exists
            self.cursor.execute("SELECT * FROM users WHERE id = %s", (record_id,))
            record = self.cursor.fetchone()
            
            if not record:
                print("Record not found!")
                return
            
            print("\nCurrent values:")
            print(f"1. Name: {record[1]}")
            print(f"2. Age: {record[2]}")
            print(f"3. Email: {record[3]}")
            
            field = input("\nWhich field do you want to edit (1-3)? ")
            new_value = input("Enter new value: ")
            
            if field == "1":
                query = "UPDATE users SET name = %s WHERE id = %s"
            elif field == "2":
                query = "UPDATE users SET age = %s WHERE id = %s"
            elif field == "3":
                query = "UPDATE users SET email = %s WHERE id = %s"
            else:
                print("Invalid field selection!")
                return
            
            self.cursor.execute(query, (new_value, record_id))
            self.connection.commit()
            print("Record updated successfully!")
        except Error as e:
            print(f"Error editing record: {e}")

    def delete_record(self):
        try:
            record_id = input("Enter the ID of the record to delete: ")
            
            # Check if record exists
            self.cursor.execute("SELECT * FROM users WHERE id = %s", (record_id,))
            if not self.cursor.fetchone():
                print("Record not found!")
                return
            
            confirm = input("Are you sure you want to delete this record? (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
            
            self.cursor.execute("DELETE FROM users WHERE id = %s", (record_id,))
            self.connection.commit()
            print("Record deleted successfully!")
        except Error as e:
            print(f"Error deleting record: {e}")

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")

def main():
    db = DatabaseManager()
    
    while True:
        print("\nDatabase Operations Menu:")
        print("1. Add Record")
        print("2. View Records")
        print("3. Edit Record")
        print("4. Delete Record")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            db.add_record()
        elif choice == '2':
            db.view_records()
        elif choice == '3':
            db.edit_record()
        elif choice == '4':
            db.delete_record()
        elif choice == '5':
            db.close_connection()
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()