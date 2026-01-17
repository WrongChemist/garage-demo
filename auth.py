from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session or not session["user"].get("is_admin"):
            flash("Admin access required")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper
