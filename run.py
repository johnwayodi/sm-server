"""Runs the Application using development configuration"""
from storemanager import create_app

app = create_app("development")

if __name__ == '__main__':
    app.run()
