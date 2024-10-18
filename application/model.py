from application.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(10), nullable=False)
    approved = db.Column(db.Boolean(), default=False)
    Address = db.Column(db.String(60), unique=True, nullable=True)
    pin = db.Column(db.Integer, unique=True, nullable=True)
   
    roles = db.relationship('Role', secondary='user_role', backref=db.backref('users', lazy=True))
    customer_dets = db.relationship('Customer', backref='user', lazy=True, uselist=False)
    professional_dets = db.relationship('ServiceProfessional', backref='user', lazy=True, uselist=False)

class Customer(db.Model):
    table_id = db.Column(db.Integer, primary_key=True)  # Keeping as table_id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    pin = db.Column(db.Integer, unique=True, nullable=True)
    service_requests = db.relationship('ServiceRequest', backref='customer')

class ServiceProfessional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(10), nullable=False)
    details = db.Column(db.String(200), unique=True, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    custom_price = db.Column(db.Float, nullable=True)
    
    service_requests = db.relationship('ServiceRequest', backref='service_professional')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class AdminRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class service_professional_Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.table_id'), nullable=False)  # Updated ForeignKey
    service_professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(20), nullable=False, default='requested')
    reviews = db.Column(db.String(200), nullable=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    deleted = db.Column(db.Boolean, default=False)
    custom_price = db.Column(db.Float, nullable=True)
    
    carts = db.relationship('Cart', backref='service')

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    custom_price = db.Column(db.Float, nullable=True)

    @property
    def calculate_total(self):
        if self.custom_price:
            return self.custom_price * self.quantity
        return self.service.base_price * self.quantity

    
    
    # def add_to_cart(user_id, service_id, custom_price=None, quantity=1):
    # cart_item = Cart.query.filter_by(user_id=user_id, service_id=service_id).first()
    # if cart_item:
    #     cart_item.quantity += quantity
    #     if custom_price:
    #         cart_item.custom_price = custom_price
    # else:
    #     new_cart_item = Cart(user_id=user_id, service_id=service_id, custom_price=custom_price, quantity=quantity)
    #     db.session.add(new_cart_item)
    
    # db.session.commit()
    # def update_cart_item(user_id, service_id, quantity):
    # cart_item = Cart.query.filter_by(user_id=user_id, service_id=service_id).first()
    # if cart_item:
    #     cart_item.quantity = quantity
    #     db.session.commit()
    # def delete_from_cart(user_id, service_id):
    # cart_item = Cart.query.filter_by(user_id=user_id, service_id=service_id).first()
    # if cart_item:
    #     db.session.delete(cart_item)
    #     db.session.commit()
    # def view_cart(user_id):
    # cart_items = Cart.query.filter_by(user_id=user_id).all()
    # total = sum(item.calculate_total for item in cart_items)
    
    # return {
    #     'cart_items': cart_items,
    #     'total_price': total
    # }
    
    
    



   
    
    
        
    

    

   
    
