from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message  # Import Flask-Mail
from email.mime.text import MIMEText
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brands.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Email Configuration
EMAIL_ADDRESS = "promotions.taraconnect@gmail.com"
EMAIL_PASSWORD = "mgbo stuq nykb ydgd"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)
db = SQLAlchemy(app)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    industry_category = db.Column(db.String(100), nullable=False)
    influencer_type = db.Column(db.String(100), nullable=False)
    budget_range = db.Column(db.String(50), nullable=False)


class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    social_category = db.Column(db.String(100), nullable=False)
    follower_count = db.Column(db.String(100), nullable=False)
    promo_charges = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

def sendEmail(to,name):
    content = f"""
        Hello {name},

        Welcome to TaraConnect! 

        We are excited to have you onboard.

        Best Regards,
        TaraConnect Team
        """

    msg = MIMEText(content)
    msg['From'] = 'promotions.taraconnect@gmail.com'
    msg['To'] = to
    msg['Subject'] = "Welcome to TaraConnect!"
    # Establish a secure connection using SMTP_SSL for port 465
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login('promotions.taraconnect@gmail.com', 'mgbo stuq nykb ydgd')     
    # Send the email
    server.sendmail('promotions.taraconnect@gmail.com', to, msg.as_string())
    server.quit()
    print("✅ Email sent successfully!")



@app.route('/brand', methods=['GET', 'POST'])
def for_brands():
    if request.method == 'POST':
        try:
            name = request.form.get('brand_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            industry_category = request.form.get('industry_category')
            influencer_type = request.form.get('influencer_type')
            budget_range = request.form.get('budget_range')

            print(f"✅ Received Data: {name}, {email}, {phone}, {industry_category}, {influencer_type}, {budget_range}")

            if not all([name, email, phone, industry_category, influencer_type, budget_range]):
                flash("⚠️ All fields are required!", "danger")
                return redirect(url_for('for_brands'))

            new_brand = Brand(name=name, email=email, phone=phone, 
                              industry_category=industry_category, influencer_type=influencer_type, 
                              budget_range=budget_range)
            
            db.session.add(new_brand)
            db.session.commit()
            print("✅ Brand inserted successfully!")
            flash("✅ Brand details submitted successfully!", "success")
            sendEmail(email, name)
            flash("✅ Successfully registered with TaraConnect! A confirmation email has been sent.", "success")



        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {str(e)}", "danger")
            print(f"❌ Database Insert Error: {e}")

        return redirect(url_for('for_brands'))

    return render_template('forBrands.html')

@app.route('/influencer', methods=['GET', 'POST'])
def for_influencer():
    if request.method == 'POST':
        try:
            name = request.form.get('influencer_name')
            email = request.form.get('influ_email')
            phone = request.form.get('phone')
            social_category = request.form.get('social_category')
            follower_count = request.form.get('follower_count')
            promo_charges = request.form.get('promo_charges')

            print(f"✅ Influencer Data Received: {name}, {email}, {phone}, {social_category}, {follower_count}, {promo_charges}")

            if not all([name, email, phone, social_category, follower_count, promo_charges]):
                flash("⚠️ All fields are required!", "danger")
                return redirect(url_for('for_influencer'))

            # ORM approach for inserting influencer data
            new_influencer = Influencer(
                name=name, email=email, phone=phone, 
                social_category=social_category, follower_count=follower_count, 
                promo_charges=promo_charges
            )

            db.session.add(new_influencer)
            db.session.commit()
            print("✅ Influencer inserted successfully!")
            flash("✅ Influencer details submitted successfully!", "success")
            sendEmail(email, name)
            flash("✅ Successfully registered with TaraConnect! A confirmation email has been sent.", "success")



        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error: {str(e)}", "danger")
            print(f"❌ Database Insert Error: {e}")

        return redirect(url_for('for_influencer'))

    return render_template('forInfluencer.html')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
