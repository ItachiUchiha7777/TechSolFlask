from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Service categories data
SERVICES_DATA = {
    'smart_home': {
        'title': 'Smart Home',
        'icon': 'fas fa-home',
        'services': ['Thermostat', 'Video Doorbells', 'Hubs & Speakers', 'Garage Doors']
    },
    'audio_video': {
        'title': 'Audio & Video',
        'icon': 'fas fa-video',
        'services': ['Home Theater', 'Universal Remote', 'Advanced Audio Systems', 'Gaming Console Setup']
    },
    'around_home': {
        'title': 'Around The Home',
        'icon': 'fas fa-hammer',
        'services': ['Wall Hanging', 'Light Bulb Changing', 'Furniture Assembly', 'Holiday Light Hanging / Removal', 'Yard Clean-up', 'General Handyman']
    },
    'wifi_network': {
        'title': 'WiFi & Network',
        'icon': 'fas fa-wifi',
        'services': ['Routers', 'In-Wall Cable Running']
    },
    'home_security': {
        'title': 'Home Security',
        'icon': 'fas fa-shield-alt',
        'services': ['Cameras', 'Locks', 'Alarm Systems']
    },
    'mobile_devices': {
        'title': 'Mobile Devices',
        'icon': 'fas fa-mobile-alt',
        'services': ['Phone & Tablet']
    },
    'tv_mounting': {
        'title': 'TV Mounting',
        'icon': 'fas fa-tv',
        'services': ['TV Dismount or Remount', 'TV Mounting (up to 32")', 'TV Mounting (33"-60")', 'TV Mounting (61" or larger)', 'TV Wire In-Wall Concealment']
    },
    'computers_printers': {
        'title': 'Computers & Printers',
        'icon': 'fas fa-desktop',
        'services': ['Computers', 'Printers']
    }
}

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

@app.route('/about')
def about():
    return render_template('about.html', services_data=SERVICES_DATA)

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