from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from data import SERVICES_DATA

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Email configuration - Using environment variables
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'Itechservices87@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'Itechservices87@gmail.com')

# Initialize Flask-Mail
mail = Mail(app)

# Your existing routes remain the same...
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

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', services_data=SERVICES_DATA)

@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html", services_data=SERVICES_DATA)

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
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        
        # Get service title for display
        service_title = "Other"
        if service in SERVICES_DATA:
            service_title = SERVICES_DATA[service]['title']
        
        try:
            # Create email message
            msg = Message(
                subject=f'New Contact Form Submission - {service_title}',
                recipients=[os.environ.get('CONTACT_RECIPIENT')],
                reply_to=email
            )
            
            # Email body
            msg.body = f"""
New Contact Form Submission

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Service Needed: {service_title}

Message:
{message}

---
This message was sent from your website contact form.
"""
            
            # HTML version (optional)
            msg.html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Contact Form Submission</title>
</head>
<body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">

  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:auto; background:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
    <tr>
      <td style="background:#007BFF; padding:15px; border-top-left-radius:10px; border-top-right-radius:10px; text-align:center;">
        <h2 style="color:#ffffff; margin:0;">New Contact Form Submission</h2>
      </td>
    </tr>
    <tr>
      <td style="padding:20px;">
        <table width="100%" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
          <tr style="background:#f9f9f9;">
            <td style="font-weight:bold; width:150px;">Name:</td>
            <td>{first_name} {last_name}</td>
          </tr>
          <tr>
            <td style="font-weight:bold;">Email:</td>
            <td>{email}</td>
          </tr>
          <tr style="background:#f9f9f9;">
            <td style="font-weight:bold;">Phone:</td>
            <td>{phone}</td>
          </tr>
          <tr>
            <td style="font-weight:bold;">Service Needed:</td>
            <td>{service_title}</td>
          </tr>
        </table>

        <h3 style="margin-top:20px;">Message:</h3>
        <p style="background:#f9f9f9; padding:15px; border-radius:5px; line-height:1.5;">
          {message}
        </p>

        <hr style="margin:30px 0; border:none; border-top:1px solid #ddd;">

        <p style="font-size:12px; color:#888; text-align:center;">
          This message was sent from your website contact form.
        </p>
      </td>
    </tr>
  </table>

</body>
</html>
"""

            
            # Send email
            mail.send(msg)
            
            # Send confirmation email to customer
            confirmation_msg = Message(
                subject='Thank you for contacting I Tech Software Services',
                recipients=[email]
            )
            
            confirmation_msg.body = f"""
Dear {first_name},

Thank you for contacting I Tech Software Services. We have received your inquiry regarding {service_title}.

We will review your message and get back to you within 24 hours.

Best regards,
I Tech Software Services Team

---
This is an automated message. Please do not reply to this email.
"""
            
            mail.send(confirmation_msg)
            
            flash('Thank you! Your message has been sent successfully. We\'ll contact you soon.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
            print(f"Email error: {e}")  # For debugging
            return redirect(url_for('contact'))
    
    return render_template('contact.html', services_data=SERVICES_DATA)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', services_data=SERVICES_DATA), 404

if __name__ == '__main__':
    app.run(debug=True)