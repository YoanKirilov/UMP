import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='smartnetscan',
            database='smartnetscandb'
        )

        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                password VARCHAR(35)
            )
        """)
        self.connection.commit()

    def add_user(self, name, email, password):
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        val = (name, email, password)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print("User added successfully.")

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        val = (user_id,)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print("User deleted successfully.")

    def update_user(self, user_id, name=None, email=None, password=None):
        sql = "UPDATE users SET"
        val = []
        if name:
            sql += " name = %s,"
            val.append(name)
        if email:
            sql += " email = %s,"
            val.append(email)
        if password:
            sql += " password = %s,"
            val.append(password)
        sql = sql[:-1] + " WHERE id = %s"
        val.append(user_id)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print("User updated successfully.")
