from flask import Blueprint
from flask import current_app
from .app import create_app
from .app import login_manager
from .models import *
from .decorators import admin_required, moderator_required, permission_required
from sqlalchemy import or_,and_
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
import requests
import json
from requests.auth import HTTPBasicAuth
import unicodedata, re, itertools, sys


app = create_app()


# @app.context_processor
# def my_global_objects():
#     users = User.query.count()
#     return (users,)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/',methods=("GET", "POST"), strict_slashes=False)
def index():
    total = Room.query.order_by(Room.id.desc()).count()
    booked = Room.query.filter_by(status='Booked').order_by(Room.id.desc()).count()
    available = Room.query.filter_by(status='Vacant').order_by(Room.id.desc()).count()

                
    return render_template("main/index.html",total=total,booked=booked,available=available)

# Search results route
@app.route("/results", methods=("GET", "POST"), strict_slashes=False)
def result():
    keyword = request.form.get('sval')

    if request.method == 'POST':
        hostels = Hostel.query.filter(or_(Hostel.name.ilike(f'%{keyword}%'), Hostel.location.ilike(f'%{keyword}%'))).all()
        available = Room.query.filter_by(status='Vacant').order_by(Room.id.desc()).all()
        return render_template("main/action.html",hostels=hostels,Room=Room,available=available)

    else:
        hostels = Hostel.query.order_by(Hostel.id.desc()).all()
        available = Room.query.filter_by(status='Vacant').order_by(Room.id.desc()).all()

        return render_template("main/action.html",hostels=hostels,Room=Room,available=available)

    return render_template("main/action.html",hostels=hostels,Room=Room,available=available)



@app.route("/booking/<int:hostel_id>/<int:room_id>/", methods=("GET", "POST"), strict_slashes=False)
def booking(hostel_id,room_id):

    hostel = Hostel.query.filter_by(id=hostel_id).first()
    room = Room.query.filter_by(id=room_id).first()

    return render_template("main/booking.html",hostel=hostel,room=room)

# Handle Errors
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
    app.run(debug=True,threaded=True)
