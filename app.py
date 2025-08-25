from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Service categories data with images
SERVICES_DATA = {
    'smart_home': {
        'title': 'Smart Home',
        'icon': 'fas fa-home',
        'services': ['Thermostat', 'Video Doorbells', 'Hubs & Speakers', 'Garage Doors'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1586953208448-b95a79798f07?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1545259741-2ea3ebf61fa0?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1556075798-4825dfaaf498?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'audio_video': {
        'title': 'Audio & Video',
        'icon': 'fas fa-video',
        'services': ['Home Theater', 'Universal Remote', 'Advanced Audio Systems', 'Gaming Console Setup'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1493020258366-be3ead61c85c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'around_home': {
        'title': 'Around The Home',
        'icon': 'fas fa-hammer',
        'services': ['Wall Hanging', 'Light Bulb Changing', 'Furniture Assembly', 'Holiday Light Hanging / Removal', 'Yard Clean-up', 'General Handyman'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1563453392212-326f5e854473?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1609585058196-31c2c2b4ad96?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'wifi_network': {
        'title': 'WiFi & Network',
        'icon': 'fas fa-wifi',
        'services': ['Routers', 'In-Wall Cable Running'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1544717302-de2939b7ef71?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1544717302-de2939b7ef71?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1606904825846-647eb07f5be2?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'home_security': {
        'title': 'Home Security',
        'icon': 'fas fa-shield-alt',
        'services': ['Cameras', 'Locks', 'Alarm Systems'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1582139329536-e7284fece509?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1558036117-15d82a90b9b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'mobile_devices': {
        'title': 'Mobile Devices',
        'icon': 'fas fa-mobile-alt',
        'services': ['Phone & Tablet'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1565849904461-04a58ad377e0?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1580910051074-3eb694886505?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'tv_mounting': {
        'title': 'TV Mounting',
        'icon': 'fas fa-tv',
        'services': ['TV Dismount or Remount', 'TV Mounting (up to 32")', 'TV Mounting (33"-60")', 'TV Mounting (61" or larger)', 'TV Wire In-Wall Concealment'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1567690187548-f07b1d7bf5a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
    },
    'computers_printers': {
        'title': 'Computers & Printers',
        'icon': 'fas fa-desktop',
        'services': ['Computers', 'Printers'],
        'images': {
            'main': 'https://images.unsplash.com/photo-1547394765-185e1e68f34e?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'thumbnails': [
                'https://images.unsplash.com/photo-1547394765-185e1e68f34e?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1580910051074-3eb694886505?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
                'https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
            ]
        }
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