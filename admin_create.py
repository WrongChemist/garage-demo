from models import db, User

def create_admin(app):
    with app.app_context():
        admin_user = "admin"
        admin_pass = "secret123"

        if not (User.query.filter_by(username=admin_user).first()):
            admin = User(username=admin_user, is_admin=True)
            admin.set_password(admin_pass)
            db.session.add(admin)
            db.session.commit()
