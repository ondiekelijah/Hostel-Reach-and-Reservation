from flask import Blueprint
from flask import current_app
from .app import create_app
from .app import login_manager
from .models import *
from .decorators import admin_required, moderator_required, permission_required

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
)
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

app = create_app()


# @app.context_processor
# def my_global_objects():
#     global_hostels = Hostel.query.with_entities(Hostel.name, Hostel.id)
#     jibu = dict(global_hostels)
#     print(jibu)
#     return jibu

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def reroute():
    return redirect(url_for('auth.login'))

@app.route('/main')
def index():
    return render_template("index.html")

@app.route('/edit')
def edit():
    return render_template("edit_user.html")

@app.errorhandler(400)
def bad_request(e):
    return render_template("errors/400.html", title="Bad Request"), 400


@app.errorhandler(401)
def unauthorised(e):
    return render_template("errors/401.html", title="Unauthorised"), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html", title="Forbidden"), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html", title="Page Not Found"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html", title="Internal Server Error"), 500


@app.errorhandler(408)
def request_time_out(e):
    return render_template("errors/408.html", title="Request Time-Out"), 408


@app.errorhandler(501)
def not_implemented(e):
    return render_template("errors/501.html", title="Not Implemented"), 501


@app.errorhandler(502)
def service_temporarily_overloaded(e):
    return (
        render_template("errors/502.html", title="Service Temporarily Overloaded"),
        502,
    )


@app.errorhandler(503)
def service_unavailable(e):
    return render_template("errors/503.html", title="Service Unavailable"), 503


if __name__ == "__main__":
    app.run(debug=True)
