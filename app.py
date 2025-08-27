from flask import Flask, render_template, request, jsonify
import os
from data import SERVICES_DATA

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Service categories data with detailed information


@app.route('/')
def index():
    return render_template('index.html', services_data=SERVICES_DATA)

@app.route('/services')
def services():
    return render_template('services.html', services_data=SERVICES_DATA)

@app.route('/services/<category>')
def service_category(category):
    if category in SERVICES_DATA:
        return render_template('service_detail.html', 
                             category=category, 
                             service_data=SERVICES_DATA[category],
                             services_data=SERVICES_DATA)
    return render_template('404.html'), 404
@app.route('/partner')
def partner():
    return render_template('partner.html', services_data=SERVICES_DATA)

@app.route('/service/<category>/<service_name>')
def service_detail(category, service_name):
    if (category in SERVICES_DATA and 
        service_name in SERVICES_DATA[category]['services']):
        return render_template('individual_service.html',
                             category=category,
                             service_name=service_name,
                             service_info=SERVICES_DATA[category]['services'][service_name],
                             services_data=SERVICES_DATA)
    return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html', services_data=SERVICES_DATA)

@app.route('/faq')
def faq():
    return render_template('faq.html', services_data=SERVICES_DATA)

@app.route('/terms')
def terms():
    return render_template('terms.html', services_data=SERVICES_DATA)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        data = {
            'first_name': request.form.get('firstName'),
            'last_name': request.form.get('lastName'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'service': request.form.get('service'),
            'message': request.form.get('message')
        }
        
        # Here you would typically save to database or send email
        # For now, we'll just return a success response
        if request.is_json or request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': True, 'message': 'Thank you! We\'ll contact you soon.'})
        else:
            return render_template('contact_success.html', services_data=SERVICES_DATA)
    
    return render_template('contact.html', services_data=SERVICES_DATA)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', services_data=SERVICES_DATA), 404

if __name__ == '__main__':
    app.run(debug=True)