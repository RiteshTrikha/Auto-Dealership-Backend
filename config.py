class Config:
    # database configurations
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootpassword@db/DealershipDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'Dealership API',
        'uiversion': 3
    }
    # debug mode
    DEBUG = True

    # JWT configurations
    JWT_SECRET_KEY = 'secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    # swagger configurations
    
    SWAGGER = {
        'title': 'My API',
        'uiversion': 3,
        "openapi": "3.0.2",
        "specs_route": "/",
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [{"BearerAuth": []}]
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootpassword@localhost:3307/DealershipDB'

    JWT_SECRET = 'secret_key'