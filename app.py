from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from sqlalchemy.exc import IntegrityError, OperationalError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lecture_notes.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            try:
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, password=hashed_password, role=role)
                db.session.add(new_user)
                db.session.commit()
                flash('Registered successfully. Please log in.', 'success')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'lecturer':
        return redirect(url_for('lecturer_dashboard'))
    else:
        return redirect(url_for('student_dashboard'))

@app.route('/lecturer/dashboard')
@login_required
def lecturer_dashboard():
    if current_user.role != 'lecturer':
        flash('Access denied. Lecturer privileges required.', 'error')
        return redirect(url_for('index'))
    recent_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.id.desc()).limit(5).all()
    return render_template('lecturer_dashboard.html', recent_notes=recent_notes)

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        flash('Access denied. Student privileges required.', 'error')
        return redirect(url_for('index'))
    
    course_filter = request.args.get('course')
    if course_filter:
        recent_notes = Note.query.filter_by(course=course_filter).order_by(Note.id.desc()).limit(10).all()
    else:
        recent_notes = Note.query.order_by(Note.id.desc()).limit(10).all()
    
    courses = db.session.query(Note.course).distinct().all()
    return render_template('student_dashboard.html', recent_notes=recent_notes, courses=courses)

from sqlalchemy.exc import OperationalError

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_notes():
    if current_user.role != 'lecturer':
        flash('Access denied. Lecturer privileges required.', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form.get('title')
        course = request.form.get('course')
        description = request.form.get('description')
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            new_note = Note(title=title, course=course, description=description, filename=filename, user_id=current_user.id)
            db.session.add(new_note)
            try:
                db.session.commit()
                flash('Note uploaded successfully.', 'success')
                return redirect(url_for('lecturer_dashboard'))
            except OperationalError:
                db.session.rollback()
                flash('Database is currently busy. Please try again.', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')
        else:
            flash('Invalid file type.', 'error')
    return render_template('upload_notes.html')

@app.route('/download/<int:note_id>')
@login_required
def download_note(note_id):
    note = Note.query.get_or_404(note_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], note.filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found.', 'error')
        return redirect(url_for('view_notes'))

@app.route('/view_notes')
@login_required
def view_notes():
    if current_user.role != 'student':
        flash('Access denied. Student privileges required.', 'error')
        return redirect(url_for('index'))
    notes = Note.query.all()
    return render_template('view_notes.html', notes=notes)

# Helper function to check if the file type is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add more routes for note upload, download, etc.

@app.route('/delete_note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    if current_user.role != 'lecturer':
        flash('Access denied. Lecturer privileges required.', 'error')
        return redirect(url_for('index'))
    
    note = Note.query.get_or_404(note_id)
    
    # Check if the current user is the owner of the note
    if note.user_id != current_user.id:
        abort(403)  # Forbidden
    
    # Delete the file from the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], note.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Delete the note from the database
    db.session.delete(note)
    db.session.commit()
    
    flash('Note deleted successfully.', 'success')
    return redirect(url_for('lecturer_dashboard'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    with app.app_context():
        db.create_all()
    app.run(debug=True)
