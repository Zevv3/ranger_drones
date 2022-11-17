# error of cant find an app or something...
# its because you didn't set flask app equal 
#  to something

import os  #python module that has functionality for folder structure
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
#The above gives access to the project from any OS we find ourselves working in
# Also allows outside files/folders to be added to the project from the base directory

load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
    Set config variables for the flask app using environment
    variables where available. Otherwise create the config 
    variable if not done already
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nana nana boo boo, you cant guess my secret key'
    # This references the SECRET_KEY variable in .env now with the load_dotenv stuff we did
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Make sure its URI in the variable here, the extension is looking specifically for that
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Turns off updates for sqlalchemy
    
    