import psycopg2

# Параметры подключения к базе данных PostgreSQL
db_params = {
    "host": "postgres",
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
}

# Функция для выполнения SQL-запросов
def execute_query(query, params=None, fetch_all=False):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
        if fetch_all:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        return result
    except psycopg2.Error as e:
        print(f"Ошибка выполнения SQL-запроса: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# Создание таблиц
def create_tables():
    create_cars_table_query = """
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        car_uid UUID UNIQUE NOT NULL,
        brand VARCHAR(80) NOT NULL,
        model VARCHAR(80) NOT NULL,
        registration_number VARCHAR(20) NOT NULL,
        power INT,
        price INT NOT NULL,
        type VARCHAR(20) CHECK (type IN ('SEDAN', 'SUV', 'MINIVAN', 'ROADSTER')),
        availability BOOLEAN NOT NULL
    );
    """
    create_rental_table_query = """
    CREATE TABLE IF NOT EXISTS rental (
        id SERIAL PRIMARY KEY,
        rental_uid UUID UNIQUE NOT NULL,
        username VARCHAR(80) NOT NULL,
        payment_uid UUID NOT NULL,
        car_uid UUID NOT NULL,
        date_from TIMESTAMP WITH TIME ZONE NOT NULL,
        date_to TIMESTAMP WITH TIME ZONE NOT NULL,
        status VARCHAR(20) NOT NULL CHECK (status IN ('IN_PROGRESS', 'FINISHED', 'CANCELED'))
    );
    """
    create_payment_table_query = """
    CREATE TABLE IF NOT EXISTS payment (
        id SERIAL PRIMARY KEY,
        payment_uid UUID NOT NULL,
        status VARCHAR(20) NOT NULL CHECK (status IN ('PAID', 'CANCELED')),
        price INT NOT NULL
    );
    """
    # Выполнение SQL-запросов
    execute_query(create_cars_table_query)
    execute_query(create_rental_table_query)
    execute_query(create_payment_table_query)

# Вызов функции для создания таблиц
create_tables()