from ext import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    password=db.Column(db.String(255))
    email=db.Column(db.String(50),unique=True)
    f_name=db.Column(db.String(50))
    l_name=db.Column(db.String(50))
    is_admin=db.Column(db.Boolean,default=False)
    is_active=db.Column(db.Boolean,default=True)
    created_at=db.Column(db.DateTime,server_default=db.func.now())
    updated_at=db.Column(db.DateTime,server_default=db.func.now(),onupdate=db.func.now())

    def __repr__(self):
        return "<User %r>" % self.email
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self,email,f_name,l_name,password, is_admin=False,is_active=True):
        self.email=email
        self.f_name=f_name
        self.l_name=l_name
        self.password=password
        self.is_admin=is_admin
        self.is_active=is_active
        db.session.commit()
