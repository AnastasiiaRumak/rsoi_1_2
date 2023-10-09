import psycopg2

class Database:
    def __init__(self):
        self.connect = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = psycopg2.connect(
                database="your_database_name",
                user="your_username",
                password="your_password",
                host="your_host",
                port="your_port"
            )
            return connection
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)
            return None

    def is_set(self, params):
        values = []
        for k, v in params.items():
            values.append(f"{k}='{v}'")
        try:
            cursor = self.connect.cursor()
            cursor.execute(f"SELECT * FROM users WHERE {' AND '.join(values)}")
            result = cursor.fetchall()
            cursor.close()
        except psycopg2.Error as e:
            return False
        return result != []

    def is_admin(self, email):
        try:
            cursor = self.connect.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND role = 'Admin'")
            result = cursor.fetchall()
            cursor.close()
        except psycopg2.Error as e:
            return False
        return result != []

    def save(self, params):
        try:
            profile = params['profile']
            email = params['email']
            role = params.get('role', 'User')

            cursor = self.connect.cursor()
            cursor.execute(f"INSERT INTO users(profile, email, role) VALUES('{profile}', '{email}', '{role}')")
            self.connect.commit()
            cursor.close()

            return "done."
        except psycopg2.Error as e:
            return False