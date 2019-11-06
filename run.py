from flask import Flask
from app import create_app
ap = create_app()
if __name__=="__main__":
    ap.run(debug=True)