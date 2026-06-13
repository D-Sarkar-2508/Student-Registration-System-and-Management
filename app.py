import os
from dotenv import load_dotenv
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret')
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'student-portal-secret-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

COLLEGE_NAME    = "DS College of Engineering & Technology"
COLLEGE_ADDRESS = "Behala, Kolkata, West Bengal - 700008"
BRANCHES = [
    'CSE', 'CSE-AIML', 'CSE-DS', 'CSE-CS', 'CSE-IoT', 'CSE-Robotics',
    'BCA( Bachelor of Computer Applications )', 'EE(Electrical Engineering)', 'EEE(Electrical and Electronics Eng.)', 'ME(Mechanical Engineering)', 'CE(Civil Engineering)', 'IT(Information Technology)',
    'BT(Biotechnology)', 'CHE(Chemical Engineering)', 'AE(Aeronautical Engineering)', 'MTech(Master of Technology)', 'MCA(Master of Computer Applications)', 'BSc-CS(Bachelor of Science in Computer Science)'
]
BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

# ── Models ─────────────────────────────────────────────────────────
class Admin(db.Model):
    __tablename__ = 'admins'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    username      = db.Column(db.String(50),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Student(db.Model):
    __tablename__ = 'students'
    id             = db.Column(db.Integer, primary_key=True)
    roll_number    = db.Column(db.String(20), unique=True, nullable=False)
    name           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(120), unique=True, nullable=False)
    password_hash  = db.Column(db.String(200), nullable=False)
    phone          = db.Column(db.String(15),  nullable=False)
    age            = db.Column(db.Integer,     nullable=True)
    branch         = db.Column(db.String(50),  nullable=False)
    year           = db.Column(db.Integer,     nullable=False)
    blood_group    = db.Column(db.String(5),   nullable=True)
    guardian_name  = db.Column(db.String(100), nullable=True)
    guardian_phone = db.Column(db.String(15),  nullable=True)
    address        = db.Column(db.String(300), nullable=True)
    registered_on  = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify_password(self, pw):
        return check_password_hash(self.password_hash, pw)


# ── Decorators ─────────────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_id'):
            flash('Admin login required.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

def current_admin():
    return Admin.query.get(session['admin_id']) if session.get('admin_id') else None

def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('student_id'):
            flash('Please log in first.', 'error')
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated

# ── Validation ─────────────────────────────────────────────────────
def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email)

def validate_phone(phone):
    return re.match(r'^\d{10}$', phone)

# ── Autocomplete APIs ──────────────────────────────────────────────
@app.route("/api/student-emails")
def api_student_emails():
    from flask import jsonify
    students = Student.query.with_entities(Student.email, Student.name).all()
    return jsonify([{"email": s.email, "name": s.name} for s in students])

@app.route("/api/admin-usernames")
def api_admin_usernames():
    from flask import jsonify
    admins = Admin.query.with_entities(Admin.username, Admin.name).all()
    return jsonify([{"username": a.username, "name": a.name} for a in admins])

# ── Landing page ───────────────────────────────────────────────────
@app.route('/')
def landing():
    return render_template('landing.html',
                           college=COLLEGE_NAME, address=COLLEGE_ADDRESS)

# ═══════════════════════════════════════════════════════════════════
#  ADMIN PORTAL
# ═══════════════════════════════════════════════════════════════════
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if session.get('admin_id'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip().lower()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')

        errors = []
        if len(name) < 2:             errors.append('Name must be at least 2 characters.')
        if len(username) < 3:         errors.append('Username must be at least 3 characters.')
        if not validate_email(email): errors.append('Enter a valid email address.')
        if len(password) < 6:         errors.append('Password must be at least 6 characters.')
        if password != confirm:       errors.append('Passwords do not match.')
        if Admin.query.filter_by(username=username).first():
            errors.append(f'Username "{username}" is already taken.')
        if Admin.query.filter_by(email=email).first():
            errors.append(f'Email "{email}" is already registered.')

        if errors:
            for e in errors: flash(e, 'error')
            return render_template('admin/signup.html', form=request.form)

        admin = Admin(name=name, username=username, email=email)
        admin.password = password
        db.session.add(admin)
        db.session.commit()
        flash(f'Account created! Welcome, {name}. Please log in.', 'success')
        return redirect(url_for('admin_login'))

    return render_template('admin/signup.html', form={})


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_id'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.verify_password(password):
            session['admin_id'] = admin.id
            flash(f'Welcome, {admin.name}!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Admin logged out.', 'info')
    return redirect(url_for('landing'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    admin    = current_admin()
    total    = Student.query.count()
    by_year  = {y: Student.query.filter_by(year=y).count() for y in [1,2,3,4]}
    by_branch= {}
    for b in BRANCHES:
        c = Student.query.filter_by(branch=b).count()
        if c: by_branch[b] = c
    recent = Student.query.order_by(Student.registered_on.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
                           admin=admin, total=total,
                           by_year=by_year, by_branch=by_branch, recent=recent)


@app.route('/admin/students')
@admin_required
def admin_students():
    admin         = current_admin()
    search        = request.args.get('search', '').strip()
    branch_filter = request.args.get('branch', '').strip()
    year_filter   = request.args.get('year', '').strip()
    q = Student.query
    if search:
        q = q.filter(db.or_(
            Student.name.ilike(f'%{search}%'),
            Student.roll_number.ilike(f'%{search}%'),
            Student.email.ilike(f'%{search}%')
        ))
    if branch_filter:
        q = q.filter_by(branch=branch_filter)
    if year_filter:
        q = q.filter_by(year=int(year_filter))
    students = q.order_by(Student.registered_on.desc()).all()
    return render_template('admin/students.html',
                           admin=admin, students=students, branches=BRANCHES,
                           search=search, branch_filter=branch_filter,
                           year_filter=year_filter, total=Student.query.count())


@app.route('/admin/students/<int:sid>')
@admin_required
def admin_view_student(sid):
    admin = current_admin()
    s = Student.query.get_or_404(sid)
    return render_template('admin/view_student.html', admin=admin, student=s,
                           college=COLLEGE_NAME, address=COLLEGE_ADDRESS)


@app.route('/admin/students/add', methods=['GET', 'POST'])
@admin_required
def admin_add_student():
    admin = current_admin()
    if request.method == 'POST':
        errors = []
        name        = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip().upper()
        email       = request.form.get('email', '').strip().lower()
        phone       = request.form.get('phone', '').strip()
        branch      = request.form.get('branch', '')
        year        = request.form.get('year', '')
        password    = request.form.get('password', '')

        if len(name) < 2:        errors.append('Name must be at least 2 characters.')
        if len(roll_number) < 3: errors.append('Roll number too short.')
        if not validate_email(email):  errors.append('Invalid email.')
        if not validate_phone(phone):  errors.append('Phone must be 10 digits.')
        if not branch:           errors.append('Select a branch.')
        if not year:             errors.append('Select a year.')
        if len(password) < 6:   errors.append('Password must be at least 6 characters.')
        if Student.query.filter_by(roll_number=roll_number).first():
            errors.append(f'Roll number {roll_number} already exists.')
        if Student.query.filter_by(email=email).first():
            errors.append(f'Email {email} already exists.')

        if errors:
            for e in errors: flash(e, 'error')
            return render_template('admin/student_form.html', admin=admin,
                                   form=request.form, edit=False,
                                   branches=BRANCHES, blood_groups=BLOOD_GROUPS)

        s = Student(
            roll_number=roll_number, name=name, email=email,
            phone=phone, branch=branch, year=int(year),
            age=request.form.get('age') or None,
            blood_group=request.form.get('blood_group') or None,
            guardian_name=request.form.get('guardian_name', '').strip() or None,
            guardian_phone=request.form.get('guardian_phone', '').strip() or None,
            address=request.form.get('address', '').strip() or None,
        )
        s.password = password
        db.session.add(s)
        db.session.commit()
        flash(f'Student {name} added successfully!', 'success')
        return redirect(url_for('admin_students'))

    return render_template('admin/student_form.html', admin=admin,
                           form={}, edit=False,
                           branches=BRANCHES, blood_groups=BLOOD_GROUPS)


@app.route('/admin/students/edit/<int:sid>', methods=['GET', 'POST'])
@admin_required
def admin_edit_student(sid):
    admin = current_admin()
    s = Student.query.get_or_404(sid)
    if request.method == 'POST':
        errors = []
        name        = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip().upper()
        email       = request.form.get('email', '').strip().lower()
        phone       = request.form.get('phone', '').strip()
        branch      = request.form.get('branch', '')
        year        = request.form.get('year', '')

        if len(name) < 2:       errors.append('Name too short.')
        if not validate_email(email): errors.append('Invalid email.')
        if not validate_phone(phone): errors.append('Phone must be 10 digits.')

        dup_roll = Student.query.filter_by(roll_number=roll_number).first()
        if dup_roll and dup_roll.id != sid:
            errors.append('Roll number already taken.')
        dup_email = Student.query.filter_by(email=email).first()
        if dup_email and dup_email.id != sid:
            errors.append('Email already taken.')

        if errors:
            for e in errors: flash(e, 'error')
            return render_template('admin/student_form.html', admin=admin,
                                   form=request.form, edit=True, student=s,
                                   branches=BRANCHES, blood_groups=BLOOD_GROUPS)

        s.name = name; s.roll_number = roll_number; s.email = email
        s.phone = phone; s.branch = branch; s.year = int(year)
        s.age           = request.form.get('age') or None
        s.blood_group   = request.form.get('blood_group') or None
        s.guardian_name = request.form.get('guardian_name', '').strip() or None
        s.guardian_phone= request.form.get('guardian_phone', '').strip() or None
        s.address       = request.form.get('address', '').strip() or None

        new_pw = request.form.get('password', '').strip()
        if new_pw:
            if len(new_pw) < 6:
                flash('New password must be at least 6 characters.', 'error')
                return render_template('admin/student_form.html', admin=admin,
                                       form=request.form, edit=True, student=s,
                                       branches=BRANCHES, blood_groups=BLOOD_GROUPS)
            s.password = new_pw

        db.session.commit()
        flash(f'Student {name} updated!', 'success')
        return redirect(url_for('admin_students'))

    return render_template('admin/student_form.html', admin=admin,
                           form={
                               'name': s.name, 'roll_number': s.roll_number,
                               'email': s.email, 'phone': s.phone,
                               'branch': s.branch, 'year': s.year,
                               'age': s.age, 'blood_group': s.blood_group,
                               'guardian_name': s.guardian_name,
                               'guardian_phone': s.guardian_phone,
                               'address': s.address,
                           }, edit=True, student=s,
                           branches=BRANCHES, blood_groups=BLOOD_GROUPS)


@app.route('/admin/students/delete/<int:sid>', methods=['POST'])
@admin_required
def admin_delete_student(sid):
    s = Student.query.get_or_404(sid)
    name = s.name
    db.session.delete(s)
    db.session.commit()
    flash(f'Student {name} deleted.', 'info')
    return redirect(url_for('admin_students'))


# ═══════════════════════════════════════════════════════════════════
#  STUDENT PORTAL
# ═══════════════════════════════════════════════════════════════════
@app.route('/student')
def student_home():
    return render_template('student/home.html', college=COLLEGE_NAME)


@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if session.get('student_id'):
        return redirect(url_for('student_dashboard'))
    if request.method == 'POST':
        errors = []
        name        = request.form.get('name', '').strip()
        roll_number = request.form.get('roll_number', '').strip().upper()
        email       = request.form.get('email', '').strip().lower()
        phone       = request.form.get('phone', '').strip()
        branch      = request.form.get('branch', '')
        year        = request.form.get('year', '')
        password    = request.form.get('password', '')
        confirm     = request.form.get('confirm', '')

        if len(name) < 2:           errors.append('Name must be at least 2 characters.')
        if len(roll_number) < 3:    errors.append('Roll number too short.')
        if not validate_email(email): errors.append('Invalid email address.')
        if not validate_phone(phone): errors.append('Phone must be 10 digits.')
        if not branch:              errors.append('Please select a branch.')
        if not year:                errors.append('Please select your year.')
        if len(password) < 6:       errors.append('Password must be at least 6 characters.')
        if password != confirm:     errors.append('Passwords do not match.')
        if Student.query.filter_by(roll_number=roll_number).first():
            errors.append('Roll number already registered.')
        if Student.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        if errors:
            for e in errors: flash(e, 'error')
            return render_template('student/register.html',
                                   form=request.form, branches=BRANCHES,
                                   blood_groups=BLOOD_GROUPS)

        s = Student(
            roll_number=roll_number, name=name, email=email,
            phone=phone, branch=branch, year=int(year),
            age=request.form.get('age') or None,
            blood_group=request.form.get('blood_group') or None,
            guardian_name=request.form.get('guardian_name', '').strip() or None,
            guardian_phone=request.form.get('guardian_phone', '').strip() or None,
            address=request.form.get('address', '').strip() or None,
        )
        s.password = password
        db.session.add(s)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('student_login'))

    return render_template('student/register.html',
                           form={}, branches=BRANCHES, blood_groups=BLOOD_GROUPS)


@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if session.get('student_id'):
        return redirect(url_for('student_dashboard'))
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        s = Student.query.filter_by(email=email).first()
        if s and s.verify_password(password):
            session['student_id'] = s.id
            flash(f'Welcome, {s.name}!', 'success')
            return redirect(url_for('student_dashboard'))
        flash('Invalid email or password.', 'error')
    return render_template('student/login.html')


@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('student_home'))


@app.route('/student/dashboard')
@student_required
def student_dashboard():
    s = Student.query.get(session['student_id'])
    return render_template('student/dashboard.html', student=s,
                           college=COLLEGE_NAME, address=COLLEGE_ADDRESS)


@app.route('/student/update', methods=['GET', 'POST'])
@student_required
def student_update():
    s = Student.query.get(session['student_id'])
    if request.method == 'POST':
        errors = []
        phone   = request.form.get('phone', '').strip()
        if not validate_phone(phone): errors.append('Phone must be 10 digits.')
        g_phone = request.form.get('guardian_phone', '').strip()
        if g_phone and not validate_phone(g_phone):
            errors.append('Guardian phone must be 10 digits.')
        age = request.form.get('age', '').strip()
        if age and (not age.isdigit() or not (15 <= int(age) <= 50)):
            errors.append('Age must be between 15 and 50.')
        if errors:
            for e in errors: flash(e, 'error')
            return render_template('student/update.html', student=s,
                                   blood_groups=BLOOD_GROUPS)
        s.phone          = phone
        s.age            = int(age) if age else None
        s.blood_group    = request.form.get('blood_group') or s.blood_group
        s.guardian_name  = request.form.get('guardian_name', '').strip() or None
        s.guardian_phone = g_phone or None
        s.address        = request.form.get('address', '').strip() or None
        new_pw = request.form.get('new_password', '').strip()
        if new_pw:
            if len(new_pw) < 6:
                flash('New password must be at least 6 characters.', 'error')
                return render_template('student/update.html', student=s,
                                       blood_groups=BLOOD_GROUPS)
            s.password = new_pw
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student_dashboard'))
    return render_template('student/update.html', student=s,
                           blood_groups=BLOOD_GROUPS)


@app.route('/student/id-card')
@student_required
def student_id_card():
    s = Student.query.get(session['student_id'])
    return render_template('student/id_card.html', student=s,
                           college=COLLEGE_NAME, address=COLLEGE_ADDRESS)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
