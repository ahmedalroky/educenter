User Management Routes (/app/api/user_routes.py)
POST /users/login: Authenticate a user and return a session token.
POST /users/signup: Register a new user account.
GET /users/{user_id}: Retrieve a specific user's profile information.
PUT /users/{user_id}: Update a specific user's profile information.
DELETE /users/{user_id}: Delete a specific user account.


School Management Routes (/app/api/school_routes.py)
GET /schools: List all schools.
POST /schools: Create a new school.
GET /schools/{school_id}: Retrieve details of a specific school.
PUT /schools/{school_id}: Update details of a specific school.
DELETE /schools/{school_id}: Delete a specific school.


Subject Management Routes (/app/api/subject_routes.py)
GET /subjects: List all subjects.
POST /subjects: Add a new subject to the catalog.
GET /subjects/{subject_id}: Retrieve details of a specific subject.
PUT /subjects/{subject_id}: Update information of a specific subject.
DELETE /subjects/{subject_id}: Remove a subject from the catalog.


Class Session Management Routes (/app/api/class_session_routes.py)
GET /class_sessions: List all class sessions.
POST /class_sessions: Schedule a new class session.
GET /class_sessions/{class_id}: Get details of a specific class session.
PUT /class_sessions/{class_id}: Update details of a specific class session.
DELETE /class_sessions/{class_id}: Cancel a specific class session.


Enrollment Management Routes (/app/api/enrollment_routes.py)
POST /enrollments: Enroll a student in a class session.
GET /enrollments/student/{student_id}: List all class sessions a student is enrolled in.
DELETE /enrollments/{enrollment_id}: Withdraw a student from a class session.


Notification Management Routes (/app/api/notification_routes.py)
GET /notifications/user/{user_id}: Retrieve all notifications for a specific user.
POST /notifications/user/{user_id}: Create a new notification for a user.
PUT /notifications/{notification_id}: Mark a notification as read.
