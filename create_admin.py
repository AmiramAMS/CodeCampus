# create_admin.py
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = 'admin'
    password = 'admin123'

    if not User.query.filter_by(username=username).first():
        user = User(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()
        print("Admin user '{username}' created.")
    else:
        print("Admin user '{username}' already exists.")
