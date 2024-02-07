import mysql.connector
from mysql.connector import Error
# Adjust the import path according to your project structure
from config.settings import Config

def create_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database `{database_name}` created successfully")
    except Error as e:
        print(f"Error creating database: {e}")

def create_table(connection, create_table_sql):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def main():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            passwd=Config.DB_PASSWORD
        )
        if connection.is_connected():
            print("MySQL Database connection successful")
            
            create_database(connection, Config.DB_NAME)
            
            # Switch to the newly created database
            connection.database = Config.DB_NAME
            
            # SQL commands to create tables
            create_table_commands = [
                """
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('student', 'teacher', 'admin') NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS Profiles (
                    profile_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(255),
                    bio TEXT,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS Schools (
                    school_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address TEXT NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS Subjects (
                    subject_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS ClassSessions (
                    class_id INT AUTO_INCREMENT PRIMARY KEY,
                    subject_id INT NOT NULL,
                    teacher_id INT NOT NULL,
                    day VARCHAR(10) NOT NULL,
                    time TIME NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
                    FOREIGN KEY (teacher_id) REFERENCES Users(user_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS Enrollments (
                    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    class_id INT NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES Users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (class_id) REFERENCES ClassSessions(class_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS Notifications (
                    notification_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    read_status BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
                );
                """
            ]
            
            for command in create_table_commands:
                create_table(connection, command)
                
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()
