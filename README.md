# Lecture Notes Management System

## Description
The Lecture Notes Management System is a web-based application designed to facilitate the sharing of lecture notes between lecturers and students. It provides a platform for lecturers to upload their notes and for students to access and download them.

## Features
- User authentication (Student and Lecturer roles)
- Lecturers can upload lecture notes
- Students can view and download lecture notes
- Responsive design for both desktop and mobile devices
- Search functionality for notes (if implemented)
- User-friendly interface

## Technologies Used
- Python
- Flask (Web Framework)
- SQLite (Database)
- HTML/CSS
- JavaScript
- Git (Version Control)

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/TemitopeGX/lecture-notes-management-system.git
   cd lecture-notes-management-system
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db upgrade
   ```

5. Run the application:
   ```
   flask run
   ```

6. Open a web browser and navigate to `http://localhost:5000`

## Usage
1. Register as either a student or a lecturer.
2. Log in to access your dashboard.
3. Lecturers can upload notes from their dashboard.
4. Students can view and download available notes.



## Project Structure
lecture-notes-management-system/
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ └── utils.py
├── static/
│ ├── css/
│ │ └── style.css
│ └── js/
│ └── script.js
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── lecturer_dashboard.html
│ ├── student_dashboard.html
│ ├── upload_notes.html
│ └── view_notes.html
├── .gitignore
├── config.py
├── requirements.txt
└── run.py



## Contributing
Contributions to the Lecture Notes Management System are welcome. Please follow these steps to contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - [temitopeayomikun999@gmail.com](mailto:temitopeayomikun999@gmail.com)

Project Link: [https://github.com/TemitopeGX/lecture-notes-management-system](https://github.com/TemitopeGX/lecture-notes-management-system)

## Acknowledgements
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [GitHub Pages](https://pages.github.com)
