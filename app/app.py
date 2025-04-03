from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from modules import User, get_db_connection, bcrypt
from my_secret import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY  # Use the secret key from my_secret.py


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Add this function to fix the error
@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user_by_username(username)  

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username, email or password', 'flash-danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        result = User.register_user(username, email, password)

        if result == "User registered successfully.":
            flash(result, 'success')
            return redirect(url_for('login'))
        else:
            flash('The username or email is already taken.', 'flash-warning')
            return redirect(url_for('register'))  # Redirect to show the warning

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "flash-success")
    return redirect(url_for('index'))

# Route for updating profile settings
@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form['username']
    email = request.form['email']
    bio = request.form['bio']

    # Update user profile in the database
    result = User.update_user_info(current_user.id, username, email, bio, current_user.phone, current_user.language)

    if result:
        flash("Profile updated successfully!", "flash-success")
    else:
        flash("An error occurred while updating your profile.", "flash-danger")

    return redirect(url_for('dashboard'))

# Route for updating account settings
@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    phone = request.form['phone']
    language = request.form['language']

    # Update user account settings in the database
    result = User.update_user_info(current_user.id, current_user.username, current_user.email, current_user.bio, phone, language)

    if result:
        flash("Account settings updated successfully!", "flash-success")
    else:
        flash("An error occurred while updating your account settings.", "flash-danger")

    return redirect(url_for('dashboard'))

# Route for updating security settings (password & 2FA)
@app.route('/update_security', methods=['POST'])
@login_required
def update_security():
    password = request.form['password']
    two_factor = request.form['two_factor']

    # Update user password if provided
    if password:
        result = User.update_user_password(current_user.id, password)
        if result:
            flash("Password updated successfully!", "flash-success")
        else:
            flash("An error occurred while updating your password.", "flash-danger")
    
    # Update two-factor authentication setting
    result = User.update_user_2fa(current_user.id, two_factor)

    if result:
        flash("Security settings updated successfully!", "flash-success")
    else:
        flash("An error occurred while updating your security settings.", "flash-danger")
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
