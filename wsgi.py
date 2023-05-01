
from app import  app
from script import db_setup
if __name__ == "__main__":
        db_setup()
        app.run()