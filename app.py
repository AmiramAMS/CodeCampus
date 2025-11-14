from flask import (
    Flask, request, jsonify, render_template,
    url_for, redirect, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import io, sys, os, platform, subprocess, tempfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ------ Models ------
class User(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(150), nullable=False, unique=True)
    password  = db.Column(db.String(150), nullable=False)
    is_admin  = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

class Solution(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer)
    code        = db.Column(db.Text)
    language    = db.Column(db.String(50))
    passed      = db.Column(db.Boolean)
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='solutions')

class Question(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default='easy')

with app.app_context():
    db.create_all()

# ------ Context Processor ------
@app.context_processor
def inject_globals():
    username = None
    if 'user_id' in session:
        u = User.query.get(session['user_id'])
        username = u.username if u else None
    elif session.get('guest'):
        username = 'אורח'

    is_admin = session.get('is_admin', False)
    lang     = session.get('lang', 'he')

    return dict(
        current_username=username,
        current_is_admin=is_admin,
        current_lang=lang
    )

# ------ Authentication Routes ------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('שם משתמש כבר קיים', 'danger')
            return redirect(url_for('register'))
        hashed = generate_password_hash(password)
        u = User(username, hashed)
        db.session.add(u)
        db.session.commit()
        session['user_id']  = u.id
        session['is_admin'] = u.is_admin
        flash('נרשמת בהצלחה!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User.query.filter_by(username=username).first()
        if u and check_password_hash(u.password, password):
            session['user_id']  = u.id
            session['is_admin'] = u.is_admin
            flash('!התחברת בהצלחה', 'success')
            return redirect(url_for('home'))
        flash('שם משתמש או סיסמה שגויים', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/guest_login')
def guest_login():
    session.clear()
    session['guest']    = True
    session['is_admin'] = False
    flash('!התחברת כאורח', 'info')
    return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('התנתקת מהמערכת.', 'info')
    return redirect(url_for('login'))

# ------ Language Toggle ------
@app.route('/set_language/<lang>', methods=['POST'])
def set_language(lang):
    if lang in ('he','en'):
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

# ------ Main Routes ------
@app.route('/')
def home():
    if 'user_id' not in session and 'guest' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/questions')
def questions():
    if 'user_id' not in session and 'guest' not in session:
        return redirect(url_for('login'))
    # עכשיו קורא מטבלת Question
    questions_list = [
        {'id': q.id, 'title': q.title, 'difficulty': q.difficulty}
        for q in Question.query.order_by(Question.id).all()
    ]

    return render_template("questions.html", questions_list=questions_list)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    u       = User.query.get(session['user_id'])
    solved  = Solution.query.filter_by(user_id=u.id).count()
    success = Solution.query.filter_by(user_id=u.id, passed=True).count()
    return render_template('profile.html',
                           user=u,
                           solved_count=solved,
                           success_count=success)

# ------ Inline Admin CRUD for Questions ------
@app.route('/questions/add', methods=['POST'])
def add_question_inline():
    if not session.get('is_admin'):
        return jsonify(error='unauthorized'), 403
    data  = request.get_json()
    title = data.get('title','').strip()
    diff  = data.get('difficulty','easy')
    if diff not in ('easy','medium','hard'):
        diff = 'easy'
    new_q = Question(title=title, difficulty=diff)
    db.session.add(new_q)
    db.session.commit()
    return jsonify(
        id=new_q.id,
        title=new_q.title,
        difficulty=new_q.difficulty
    ), 200

@app.route('/questions/edit', methods=['POST'])
def edit_question_inline():
    if not session.get('is_admin'):
        return jsonify(error='unauthorized'), 403
    data = request.get_json()
    qid  = data.get('id')
    q    = Question.query.get(qid)
    if not q:
        return jsonify(error='not found'), 404
    q.title      = data.get('title', q.title)
    diff = data.get('difficulty', q.difficulty)
    if diff in ('easy','medium','hard'):
        q.difficulty = diff
    db.session.commit()
    return jsonify(status='ok')

@app.route('/questions/delete', methods=['POST'])
def delete_question_inline():
    if not session.get('is_admin'):
        return jsonify(error='unauthorized'), 403
    data = request.get_json()
    qid  = data.get('id')
    q    = Question.query.get(qid)
    if q:
        db.session.delete(q)
        db.session.commit()
        return jsonify(status='ok')
    return jsonify(error='not found'), 404

# ------ Record solution (user marks solved) ------
@app.route('/record_solution', methods=['POST'])
def record_solution():
    if 'user_id' not in session:
        return jsonify(status='unauthorized'), 403
    data = request.get_json()
    sol  = Solution(
        user_id=session['user_id'],
        question_id=data['question_id'],
        code='',
        language='',
        passed=data['passed']
    )
    db.session.add(sol)
    db.session.commit()
    return jsonify(status='ok')

# ------ Run Code ------
@app.route('/run', methods=['POST'])
def run_code():
    d    = request.get_json()
    code = d.get('code','')
    lang = d.get('language','python')
    out  = io.StringIO()
    is_windows = platform.system() == 'Windows'
    
    try:
        if lang=='python':
            sys.stdout = out
            exec(code, {})
        elif lang=='java':
            # חילוץ שם המחלקה מהקוד (אם יש)
            import re
            class_match = re.search(r'public\s+class\s+(\w+)', code)
            class_name = class_match.group(1) if class_match else 'Main'
            
            # אם אין class Main, נוסיף wrapper
            if 'public class' not in code:
                code = f'public class Main {{\n    public static void main(String[] args) {{\n        {code}\n    }}\n}}'
                class_name = 'Main'
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_java = f.name
            try:
                # קומפילציה
                compile_result = subprocess.run(
                    ['javac', temp_java],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if compile_result.returncode != 0:
                    out.write(f'Compilation error: {compile_result.stderr}')
                else:
                    # הרצה - צריך להריץ מהתיקייה שבה נמצא הקובץ
                    java_dir = os.path.dirname(temp_java)
                    run_result = subprocess.run(
                        ['java', '-cp', java_dir, class_name],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    out.write(run_result.stdout)
                    if run_result.stderr:
                        out.write(f'\nError: {run_result.stderr}')
                    # מחיקת קובץ .class
                    class_file = os.path.join(java_dir, f'{class_name}.class')
                    if os.path.exists(class_file):
                        try:
                            os.remove(class_file)
                        except:
                            pass
            finally:
                if os.path.exists(temp_java):
                    try:
                        os.remove(temp_java)
                    except:
                        pass
        elif lang=='cpp':
            exe_ext = '.exe' if is_windows else ''
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_cpp = f.name
            temp_exe = temp_cpp.replace('.cpp', exe_ext)
            try:
                # קומפילציה
                if is_windows:
                    # ב-Windows, צריך להשתמש בנתיב מלא ולהמיר backslashes
                    temp_cpp_abs = os.path.abspath(temp_cpp)
                    temp_exe_abs = os.path.abspath(temp_exe)
                    # ב-Windows עם shell=True, צריך להעביר כמחרוזת
                    compile_cmd = f'g++ "{temp_cpp_abs}" -o "{temp_exe_abs}"'
                    compile_result = subprocess.run(
                        compile_cmd,
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=True
                    )
                else:
                    compile_cmd = ['g++', temp_cpp, '-o', temp_exe]
                    compile_result = subprocess.run(
                        compile_cmd,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                
                if compile_result.returncode != 0:
                    out.write(f'Compilation error: {compile_result.stderr}')
                else:
                    # הרצה
                    if is_windows:
                        # ב-Windows, צריך להשתמש בנתיב מלא
                        temp_exe_abs = os.path.abspath(temp_exe)
                        run_result = subprocess.run(
                            f'"{temp_exe_abs}"',
                            capture_output=True,
                            text=True,
                            timeout=10,
                            shell=True
                        )
                    else:
                        run_result = subprocess.run(
                            [temp_exe],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                    out.write(run_result.stdout)
                    if run_result.stderr:
                        out.write(f'\nError: {run_result.stderr}')
            finally:
                for f in [temp_cpp, temp_exe]:
                    if os.path.exists(f):
                        try:
                            os.remove(f)
                        except:
                            pass
    except subprocess.TimeoutExpired:
        out.write('Error: Code execution timeout (took too long)')
    except Exception as e:
        out.write(f'Error: {str(e)}')
    finally:
        sys.stdout = sys.__stdout__
    return jsonify(output=out.getvalue())

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
