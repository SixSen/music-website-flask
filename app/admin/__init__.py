from flask import Blueprint


admin = Blueprint("admin", __name__)
@admin.route("/")
def index():
    return "<h1 style='color:red'>this is admin</h1>"