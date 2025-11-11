from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='views', static_folder='public')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(200))
    value_description = db.Column(db.Text)
    tags = db.Column(db.String(200))  

# Routes
@app.route('/')
def home():
    # Get the 5 most recent contacts (newest first)
    recent_contacts = Contact.query.order_by(Contact.id.desc()).limit(5).all()
    return render_template('Homepage.html', recent_contacts=recent_contacts)

@app.route('/network')
def network():
    contacts = Contact.query.all()
    return render_template('Network.html', contacts=contacts)

@app.route('/guide')
def guide():
    return render_template('Guide-on-how-to-use-it.html')

@app.route('/add-contact')
def add_contact_form():
    return render_template('add-contact.html')

@app.route('/add-contact', methods=['POST'])
def add_contact_submit():
    # Get all the regular form fields
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    company = request.form.get('company')
    position = request.form.get('position')
    linkedin_url = request.form.get('linkedin_url')
    value_description = request.form.get('value_description')
    
    
    selected_tags = request.form.getlist('tags')
    
 
    tags_string = ','.join(selected_tags)
    
    # Create new contact with all fields including tags
    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company=company,
        position=position,
        linkedin_url=linkedin_url,
        value_description=value_description,
        tags=tags_string  # NEW: Save the tags
    )
    
    db.session.add(new_contact)
    db.session.commit()
    
    return redirect(url_for('network'))

@app.route('/edit-contact/<int:contact_id>')
def edit_contact_form(contact_id):
    # Find the contact by ID
    contact = Contact.query.get_or_404(contact_id)
    return render_template('edit-contact.html', contact=contact)

@app.route('/edit-contact/<int:contact_id>', methods=['POST'])
def edit_contact_submit(contact_id):
    # Find the contact to update
    contact = Contact.query.get_or_404(contact_id)
    
    # Update all fields with new data
    contact.first_name = request.form.get('first_name')
    contact.last_name = request.form.get('last_name')
    contact.email = request.form.get('email')
    contact.phone = request.form.get('phone')
    contact.company = request.form.get('company')
    contact.position = request.form.get('position')
    contact.linkedin_url = request.form.get('linkedin_url')
    contact.value_description = request.form.get('value_description')
    
    # Update tags
    selected_tags = request.form.getlist('tags')
    contact.tags = ','.join(selected_tags)
    
    # Save changes to database
    db.session.commit()
    
    return redirect(url_for('network'))

@app.route('/delete-contact/<int:contact_id>')
def delete_contact(contact_id):
    # Find the contact to delete
    contact = Contact.query.get_or_404(contact_id)
    
    # Delete from database
    db.session.delete(contact)
    db.session.commit()
    
    return redirect(url_for('network'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
