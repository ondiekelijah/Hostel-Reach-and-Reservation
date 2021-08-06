from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from auth.forms import register_form
from . import *
from wtforms import ValidationError, validators
from app import db, bcrypt, login_manager
from flask import current_app
from flask_login import (
    UserMixin,
    login_required,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from fpdf import FPDF
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
    session,
    g,
    Response,
    send_from_directory,
)
from decorators import admin_required, moderator_required, permission_required
from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from utils import *
from flask_bcrypt import generate_password_hash, check_password_hash
from models import *
from datetime import datetime
import time

reports = Blueprint("reports", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@reports.route('/reports/users')
@login_required
@admin_required
def users_report():
    users = User.query.order_by(User.id.asc()).all()
    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin
        
    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Courier", 'B' ,size = 15.0)
  
    # create a cell
    pdf.cell(200, 10, txt = "Patahao Limited", 
            ln = 1, align = 'C')
  
    # add another cell
    pdf.cell(200, 10, txt = "Users Data Report.",
            ln = 2, align = 'C')

    # add another cell
    date = datetime.now()
    today = date.today()
    d2 = today.strftime("%B %d, %Y")

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    pdf.set_font("Arial", size = 9.0)

    pdf.cell(200, 10, txt = str(d2) + "  " + str(current_time),
            ln = 1, align = 'C')

    pdf.ln(10)

    pdf.set_font('Arial', 'B', 11)
        
    col_width = page_width/3
    
    pdf.ln(1)
        
    th = 1.5 * (pdf.font_size)
    
    pdf.cell(col_width, th, 'ID', border=1)
    pdf.cell(col_width, th, 'Username', border=1)
    pdf.cell(col_width, th, 'Email', border=1)
    pdf.ln(th)

    pdf.set_font('Arial', '', 10)

    for row in users:
        pdf.cell(col_width, th, str(row.id), border=1)
        pdf.cell(col_width, th, row.uname, border=1)
        pdf.cell(col_width, th, row.email, border=1)
        pdf.ln(th)
        
    pdf.ln(15)
        
    pdf.set_font('Times','',10.0) 

    pdf.cell(200, 10, txt = "- End of report -",
            ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "© Copyright pataHao. Reports",
            ln = 2, align = 'C')

        
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=users_report.pdf'})



@reports.route('/reports/rooms')
@login_required
@admin_required
def rooms_report():

    rooms = Room.query.order_by(Room.id.asc()).all()

    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Room Data Report', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
        
    col_width = page_width/7
    
    pdf.ln(1)
        
    th = pdf.font_size
    
    for row in rooms:
        pdf.cell(col_width, th, str(row.id), border=1)
        pdf.cell(col_width, th, str(row.rent), border=1)
        pdf.cell(col_width, th, str(row.deposit), border=1)
        pdf.cell(col_width, th, row.amenities, border=1)
        pdf.cell(col_width, th, row.size, border=1)
        pdf.cell(col_width, th, row.status, border=1)
        pdf.cell(col_width, th, row.hostel.name, border=1)

        pdf.ln(th)

    pdf.ln(10)
        
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
        
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=rooms_report.pdf'})




@reports.route('/reports/hostels')
@login_required
@admin_required
def hostel_report():

    hostels = Hostel.query.order_by(Hostel.id.asc()).all()

    pdf = FPDF()
    pdf.add_page()
        
    page_width = pdf.w - 2 * pdf.l_margin
        
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Hostel Data Report', align='C')
    pdf.ln(10)

    pdf.set_font('Courier', '', 12)
        
    col_width = page_width/5
    
    pdf.ln(1)
        
    th = pdf.font_size
    
    for row in hostels:
        pdf.cell(col_width, th, str(row.name), border=1)
        pdf.cell(col_width, th, str(row.location), border=1)
        pdf.cell(col_width, th, row.management, border=1)
        pdf.cell(col_width, th, row.caretaker, border=1)
        pdf.cell(col_width, th, row.contact, border=1)

        pdf.ln(th)

        
    pdf.ln(10)
        
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
        
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=hostel_report.pdf'})

