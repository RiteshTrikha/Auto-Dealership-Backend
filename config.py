class Config:
    # database configurations
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rootpassword@db/DealershipDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER = {
        'title': 'Dealership API',
        'uiversion': 3
    }