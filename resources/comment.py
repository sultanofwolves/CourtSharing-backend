import json
from flask_restful import Resource
from flask import request
from mongoengine import DoesNotExist
from bson import ObjectId
from models.comment import Comment as Comment_model
from utils.auth import Auth

# pylint: disable=E1101
class Comment(Resource):
    
    def delete(self, id):
        # pylint: disable=E1101
        headers = request.headers
        token_validation = Auth.auth_token(headers)
        if(token_validation != 'True'):
            return token_validation
        
        try:
            Comment_model.objects.get(id=ObjectId(id)).delete()
        except DoesNotExist:
            with open('utils/errorCodes.json', 'r') as errorCodes:
                return json.load(errorCodes)['COMMENT_ERROR']['NOT_FOUND'], 500

        return True, 200
