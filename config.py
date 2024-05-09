from sqlalchemy import create_engine

class Config:
    # SSL configurations
    SSL_CA = "server-ca.pem"
    SSL_CERT = "client-cert.pem"
    SSL_KEY = "client-key.pem"

    # Database connection details
    DB_USERNAME = "backend"
    DB_PASSWORD = "backend-password"
    DB_HOST = "10.111.112.3"
    DB_NAME = "DealershipDB"

    # Database URI components
    SSL_CA_PATH = f"ssl_ca={SSL_CA}"
    SSL_CERT_PATH = f"ssl_cert={SSL_CERT}"
    SSL_KEY_PATH = f"ssl_key={SSL_KEY}"
    DB_URI = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?{SSL_CA_PATH}&{SSL_CERT_PATH}&{SSL_KEY_PATH}"

    # SQLAlchemy configurations
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_engine():
        return create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={'ssl_verify_cert': False})

    # Swagger configurations
    SWAGGER = {
        'title': 'Dealership API',
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

    # Debug mode
    DEBUG = True

    # JWT configurations
    JWT_SECRET_KEY = 'secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
