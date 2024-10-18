from flask import Flask, render_template, session
from application.database import db
from application.config import Config
from application.model import *

def create_app():
    app = Flask(__name__,template_folder='template')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)

        cust_role = Role.query.filter_by(name='customer').first()
        if not cust_role:
            cust_role = Role(name='customer')
            db.session.add(cust_role)

        ServiceProfessional = Role.query.filter_by(name='ServiceProfessional').first()
        if not ServiceProfessional:
            ServiceProfessional = Role(name  ='ServiceProfessional')
            db.session.add(ServiceProfessional)
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin',
                         email = 'admin@abc.com',
                        password = 'admin',
                        roles= [admin_role,ServiceProfessional])
            db.session.add(admin)

        db.session.commit()
        


    return app

app = create_app()

from application.routes import *

if __name__ == '__main__':
    app.run(debug=True)