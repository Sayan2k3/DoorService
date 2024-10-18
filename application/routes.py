# from main import app
# from flask import render_template, session, url_for, redirect, request ,flash
# from application.model import *

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         email = request.form.get('email', None)
#         password = request.form.get('password', None)

#         # Data Validation
#         if not email:
#             flash('Email is required')
#             return redirect(url_for('login'))
#         if not password:
#             flash('Password is required')
#             return redirect(url_for('login'))
        
#         user = User.query.filter_by(email=email).first()
#         if not user:
#             flash('Invalid email')
#             return redirect(url_for('login'))
        
#         # user_role = Role.query.filter_by(name='store_manager').first()
#         if  'ServiceProfessional' in [role.name for role in user.roles] and not user.approved:
#             flash('Your sign up request not approved! Please contact admin')
#             return redirect(url_for('login'))
        
#         if user.password == password:
#             session['username'] = user.username
#             session['role'] = [role.name for role in user.roles]
#             flash('Login Successfully')
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid password')
#             return redirect(url_for('login'))


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     session.pop('role', None)
#     return redirect(url_for('home'))


# @app.route('/signup', methods=['GET', 'POST'])
# def register():
#     return render_template('register.html')





from main import app
from flask import render_template, session, url_for, redirect, request, flash
from application.model import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        # Data Validation
        if not email:
            flash('Email is required')
            return redirect(url_for('login'))
        if not password:
            flash('Password is required')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid email')
            return redirect(url_for('login'))
        
        # Check for service professional approval
        if 'service_professional' in [role.name for role in user.roles] and not user.approved:
            flash('Your sign-up request is not approved! Please contact admin')
            return redirect(url_for('login'))
        
        if user.password == password:
            session['username'] = user.username
            session['role'] = [role.name for role in user.roles]
            flash('Login Successful')
            return redirect(url_for('home'))
        else:
            flash('Invalid password')
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        cpassword = request.form.get('cpassword', None)
        role = request.form.get('role', None)
        image = request.files.get('image', None)

        # Data Validation
        if not username:
            flash('Username is required')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('login'))
        
        if not email:
            flash('Email is required')
            return redirect(url_for('register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('login'))
        
        if not password and not cpassword:
            flash('Password is required')
            return redirect(url_for('register'))
        
        if password != cpassword:
            flash('Password and Confirm Password must be the same')
            return redirect(url_for('register'))
        
        if not role:
            flash('Role is required')
            return redirect(url_for('register'))
        
        image_file_path = None
        if image:
            image_file_path = 'images/' + image.filename
            image.save(image_file_path)
            absoulte_path = 'static/' + image_file_path
            image.save(absoulte_path)

        approved = True
        if role == 'service_professional':
            approved = False

        user = User(
            username=username,
            email=email,
            password=password,
            image_file=image_file_path,
            approved=approved,
            roles=[Role.query.filter_by(name=role).first()]
        )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    
@app.route('/user_approvals')
def user_approvals():
    approved_users = User.query.filter_by(approved=True).all()
    approved_ServiceProfessional = []
    customers = []
    for user in  approved_users:
        if 'ServiceProfessional' in [role.name for role in user.roles]:
            approved_ServiceProfessional.append(user)
        if 'customer' in [role.name for role in user.roles]:
            customers.append(user)
    approval_requests = User.query.filter_by(approved=False).all()
    return render_template('all_user_details.html', 
                           approved_ServiceProfessional=approved_ServiceProfessional,
                           customers=customers, 
                           approval_requests=approval_requests)    


@app.route('/service_categories', methods=['GET', 'POST'])
def service_categories():
    return render_template('service_categories.html')


