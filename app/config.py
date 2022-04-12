class Config:
    UPDATE_ORDER_API_URL = "http://127.0.0.1:5000/order/"

    JWT_SECRET_KEY = "aslkdmaklmq"  # FIXME: gen key properly
    JWT_ALGORITHM = "HS256"

    # TODO: move this to config file
    DB_HOST = "localhost"
    DATABASE = "e_wallet"
    USER = "hocvien_dev"
    PASSWORD = "123456"
