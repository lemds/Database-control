import sqlite3

class DatabaseController:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

    def add_record(self, name, age, email):
        try:
            self.cursor.execute('''
                INSERT INTO records (name, age, email) VALUES (?, ?, ?)
            ''', (name, age, email))
            self.connection.commit()
            print(f"Record added: {name}, {age}, {email}")
        except sqlite3.IntegrityError as e:
            print(f"Error adding record: {e}")

    def view_records(self):
        self.cursor.execute('SELECT * FROM records')
        records = self.cursor.fetchall()
        for record in records:
            print(record)

    def update_record(self, record_id, name=None, age=None, email=None):
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if age:
            fields.append("age = ?")
            values.append(age)
        if email:
            fields.append("email = ?")
            values.append(email)

        if fields:
            values.append(record_id)
            query = f"UPDATE records SET {', '.join(fields)} WHERE id = ?"
            self.cursor.execute(query, values)
            self.connection.commit()
            print(f"Record {record_id} updated.")
        else:
            print("No fields to update.")

    def delete_record(self, record_id):
        self.cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        self.connection.commit()
        print(f"Record {record_id} deleted.")

    def close_connection(self):
        self.connection.close()
        print("Database connection closed.")

# Example usage
def main():
    db = DatabaseController()

    while True:
        print("\nOptions:")
        print("1. Add record")
        print("2. View records")
        print("3. Update record")
        print("4. Delete record")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            email = input("Enter email: ")
            db.add_record(name, age, email)
        elif choice == "2":
            db.view_records()
        elif choice == "3":
            record_id = int(input("Enter record ID to update: "))
            name = input("Enter new name (or press Enter to skip): ") or None
            age = input("Enter new age (or press Enter to skip): ")
            age = int(age) if age else None
            email = input("Enter new email (or press Enter to skip): ") or None
            db.update_record(record_id, name, age, email)
        elif choice == "4":
            record_id = int(input("Enter record ID to delete: "))
            db.delete_record(record_id)
        elif choice == "5":
            db.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
