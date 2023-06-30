# 추천에 필요한 함수 추가
from crypt import methods
from flask import Blueprint, make_response, jsonify
from flask_restx import Api, Resource

from models.Book import Book # 추천에 필요한 Book테이블

recommendation = Blueprint("recommendation", __name__)
api = Api(recommendation)

# /recommend
@recommendation.route("",methods=["GET"])
def recommend_for_guest():
    
    res_obj = {
        "something": content,
        "data": {
            "customized_by_user" : result1,
            "func1":result2,
            "customized_by_wishlist" : []
        }
    }
    return make_response(jsonify(res_obj), 200)

# /recommend/{user_pk}
@recommendation.route("/<int:userId>", methods=["GET"])
def rocommend_by_user():
    
    res_obj = {
        
    }
    return make_response(jsonify(res_obj), 200)