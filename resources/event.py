from flask_restful import Resource, reqparse
from bson.json_util import dumps
from flask import request
import datetime
from models.event import Event as Event_model
from models.user import User as User_model
from models.sport import Sport as Sport_model
from mongoengine import DoesNotExist
from bson import ObjectId
import json

# pylint: disable=E1101
class Event(Resource):

    def get(self):
        args = request.args

        event_date = args.get('date')
        court_id = args.get('court')  

        try:          
            query = []
            if event_date is not None:
                query.append({"$match": {"event_date":int(event_date)}})
            if court_id is not None:
                query.append({"$match": {"court_id":int(court_id)}})
        except DoesNotExist:
            return False

        events = eval(dumps(Event_model.objects.aggregate (*query)))       
        for event in events:
            query = User_model.objects(id=event['creator']['$oid']) 
            data = query.to_json()
            creator = json.loads(data)
            event['creator'] = creator
        return events, 200
    
    def post(self):
        # TODO: validate parameters
        event_data = request.get_json(force=True, silent=True)

        new_event = Event_model(
            creation_date=datetime.datetime.now(),
            event_date=event_data['event_date'],
            title=event_data['title'],
            description=event_data['description'],
            court_id=event_data['court_id'],
            creator=User_model.objects(id=event_data['creator_id']),
            sport=Sport_model.objects(id=event_data['sport_id'])
        )
        new_event.save()
        event = new_event.to_json()
        return eval(dumps(event)), 200