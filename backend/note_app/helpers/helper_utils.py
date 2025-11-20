from dotenv import load_dotenv
import os

AES_ENCRYPTION_KEY = os.getenv('AES_ENCRYPTION_KEY')
AES_INITIALISATION_VECTOR = os.getenv('AES_INITIALISATION_VECTOR')

REDIS_USER = os.getenv('REDIS_USER')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_PORT = os.getenv('REDIS_PORT')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
