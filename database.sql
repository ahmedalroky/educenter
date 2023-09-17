CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    profile_picture VARCHAR(255),
    phone_number VARCHAR(20),
    school VARCHAR(100),
    age INT,
    grade VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    speciality VARCHAR(50),
    level VARCHAR(20)
);

CREATE TABLE teachers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    profile_picture VARCHAR(255),
    phone_number VARCHAR(20),
    school VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    location VARCHAR(100),
    article VARCHAR(255),
    grades VARCHAR(255),
    level VARCHAR(20)
);

CREATE TABLE classes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject VARCHAR(100) NOT NULL,
    day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
    time TIME,
    location VARCHAR(100),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);

CREATE TABLE student_classes (
    student_id INT,
    class_id INT,
    PRIMARY KEY (student_id, class_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (class_id) REFERENCES classes(id)
);
