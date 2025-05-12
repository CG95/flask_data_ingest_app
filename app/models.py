from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db= SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(200), nullable=False)
    created_at= db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at= db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @classmethod
    def create(cls, name, email, password):
        if not name:
            raise ValueError("Name is required")
        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is required")
        
        #encrypt the password
        encripted_password = generate_password_hash(password)
        user = cls(name=name, email=email, password=encripted_password)
        
        db.session.add(user)
        db.session.commit()
        return user
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
