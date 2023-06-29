from atexit import register
import resource
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api # Api 구현을 위함
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    
    #DB 설정
    app.config["SQLALCHEMY_DATABASE_URI"] = ""
    app.config[""]
    
    db = SQLAlchemy(app, session_options={'autocommit' : ??})
    
    # CORS 설정
    cors = CORS(app, resources={r"/*": {"origins":"*"})
                
    # EndPoint 추가
    # app.register_blueprint()
    
    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")