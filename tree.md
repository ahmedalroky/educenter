project/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── student.py
│   │   └── teacher.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── admin/
│   │   │   ├── base.html
│   │   │   ├── students/
│   │   │   │   ├── add.html
│   │   │   │   ├── edit.html
│   │   │   │   ├── list.html
│   │   │   │   └── view.html
│   │   │   ├── teachers/
│   │   │   │   ├── add.html
│   │   │   │   ├── edit.html
│   │   │   │   ├── list.html
│   │   │   │   └── view.html
│   │   │   └── admin_home.html
│   │   ├── student/
│   │   │   ├── base.html
│   │   │   ├── classes/
│   │   │   │   ├── list.html
│   │   │   │   ├── add.html
│   │   │   │   └── remove.html
│   │   │   ├── teachers/
│   │   │   │   ├── list.html
│   │   │   │   ├── add.html
│   │   │   │   └── remove.html
│   │   │   ├── profile/
│   │   │   │   └── edit.html
│   │   │   └── student_home.html
│   │   └── teacher/
│   │       ├── base.html
│   │       ├── classes/
│   │       │   ├── list.html
│   │       │   ├── add.html
│   │       │   └── remove.html
│   │       ├── students/
│   │       │   ├── list.html
│   │       │   ├── add.html
│   │       │   └── remove.html
│   │       ├── profile/
│   │       │   └── edit.html
│   │       └── teacher_home.html
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
├── config.py
├── requirements.txt
├── run.py
└── tests/
    ├── __init__.py
    ├── test_admin.py
    ├── test_student.py
    └── test_teacher.py
