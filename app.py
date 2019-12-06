from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import mongoengine
from resources.events import Events
from resources.event import Event
from resources.court import Court
from resources.courts import Courts
from resources.sport import Sport
from resources.login import Login
from resources.transport import Transport
from resources.parking import Parking
from resources.comments import Comments
from resources.comment import Comment
from resources.image import Image
from config import MONGO_URL


mongoengine.connect(alias="default", host=MONGO_URL)

APP = Flask(__name__)
CORS(APP)
API = Api(APP)


# Endpoints
API.add_resource(Events, '/events')
API.add_resource(Event, '/events/<string:id>')
API.add_resource(Login, '/login')
API.add_resource(Courts, '/courts')
API.add_resource(Court, '/courts/<string:id>')
API.add_resource(Sport, '/sports')
API.add_resource(Transport, '/transports')
API.add_resource(Parking, '/parkings')
API.add_resource(Comments, '/comments')
API.add_resource(Comment, '/comments/<string:id>')
API.add_resource(Image, '/image')

if __name__ == '__main__':
    print("Deploying service in port 5000")
    APP.run(host="0.0.0.0", port=5000, debug=True)
