from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#import blueprints/modules
from app.shared import shared_bp
from app.scheduling import scheduling_bp
from app.negotiation import negotiation_bp
from app.purchasing import purchasing_bp

app = Flask(__name__)
#register blueprints/modules
app.register_blueprint(shared_bp)
app.register_blueprint(scheduling_bp)
app.register_blueprint(negotiation_bp)
app.register_blueprint(purchasing_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)