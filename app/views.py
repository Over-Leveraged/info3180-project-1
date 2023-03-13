"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, send_from_directory
from .forms import PropertyForm
from werkzeug.utils import secure_filename
from flask import flash
from .forms import PropertyForm
from app.models import Property
import psycopg2
from app import app, db



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('properties.html')


@app.route('/test/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/properties/')
def properties():
    """Render the website's about page."""
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)
    ##return render_template('properties.html, properties=properties')

@app.route('/properties/create', methods=['POST', 'GET'])
def create():
    myform = PropertyForm()
   
    if myform.validate_on_submit():
        title = myform.title.data
        description = myform.description.data
        bedrooms = myform.bedrooms.data
        bathrooms = myform.bathrooms.data
        price = myform.price.data
        property_type = myform.property_type.data
        location = myform.location.data

        photo = myform.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            new_property = Property(title, description, bedrooms, bathrooms, location, price, property_type, filename)
            db.session.add(new_property)
            db.session.commit()
        except:
            flash('Property not listed!')
            return redirect(url_for('properties'))


        flash('Property Listed!', 'success')
        return redirect(url_for('properties'))
    return render_template('createProp.html', form=myform)

@app.route('/properties/<property_id>')
def showProperty(property_id):
    property = Property.query.get(property_id)
    return render_template('showProperty.html', property=property)



@app.route('/uploads/<filename>')
def get_image(filename):
    rootdir = os.getcwd()
    return send_from_directory(os.path.join(rootdir,app.config['UPLOAD_FOLDER']),filename)



###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
