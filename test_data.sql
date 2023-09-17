INSERT INTO students (name, profile_picture, phone_number, school, age, grade, email, speciality, level) VALUES 
    ('John Smith', 'https://example.com/profiles/john.jpg', '555-1234', 'ABC High School', 16, '10th', 'john.smith@example.com', 'Mathematics', 'Secondary'),
    ('Jane Doe', 'https://example.com/profiles/jane.jpg', '555-5678', 'XYZ High School', 17, '11th', 'jane.doe@example.com', 'English Literature', 'Secondary');

INSERT INTO teachers (name, profile_picture, phone_number, school, email, location, article, grades, level) VALUES
    ('James Johnson', 'https://example.com/profiles/james.jpg', '555-4321', 'DEF University', 'james.johnson@example.com', 'New York, NY', 'Introduction to Calculus', '9-12', 'Secondary'),
    ('Emily Davis', 'https://example.com/profiles/emily.jpg', '555-8765', 'GHI College', 'emily.davis@example.com', 'San Francisco, CA', 'Creative Writing', '9-12', 'Secondary');

INSERT INTO classes (subject, day, time, location, teacher_id) VALUES
    ('Calculus I', 'Monday', '10:00:00', 'Room 101', 1),
    ('English Literature', 'Tuesday', '11:00:00', 'Room 102', 2);

INSERT INTO student_classes (student_id, class_id) VALUES
    (1, 1),
    (1, 2),
    (2, 2);
