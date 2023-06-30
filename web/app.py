from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from apis.recommendation import recommendation
from apis.sentiment import sentiment
from apis.statistics import statistics
from apis.wordcloud import wordcloud

__USERNAME__ = "multi"
__PASSWORD__ = "multi12345!"
__HOST__ = "localhost"
DATABASE = ["USER","BOOK","MEETING"]


def create_app():
    app = Flask(__name__)
    
    #DB 설정
        # 사용할 데이터베이스의 위치
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{__USERNAME__}:{__PASSWORD__}@{__HOST__}/{DATABASE}"
        # 추가적인 메모리가 필요할 때    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        #pool
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 600 # 주어진 초 이후에 커넥션 재설정 - mysql connection이 끊기는것 방지
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10
    app.config['SQLALCHEMY_POOL_SIZE'] = 30 # 연결할 수 있는 커넥션의 수 설정
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10 # 허용된 connection 수 이상이 들어왔을 떄 몇개까지 허용?

    
    db = SQLAlchemy(app, session_options={'autocommit': True})
    
    # CORS 설정
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # EndPoint 추가
    app.register_blueprint(recommendation, url_prefix="/ml/api/recommend")
    app.register_blueprint(sentiment, url_prefix="/ml/api/book")
    app.register_blueprint(statistics, url_prefix="/ml/api/statistics")
    app.register_blueprint(wordcloud, url_prefix="/ml/api/book")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")