from dotenv import load_dotenv
import os

def pytest_configure():
    if os.getenv('CI') != 'true':
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        load_dotenv(dotenv_path=dotenv_path)