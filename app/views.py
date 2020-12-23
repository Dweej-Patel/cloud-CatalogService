from app import application, db
from app.models import Events
from flask import Response, request
import json


@application.route("/")
def index():
    rsp = Response("it works bruh", status=200, content_type="text/html")
    return rsp


@application.route("/Event", methods=["GET"])
@application.route("/Event/id/<id>", methods=["GET"])
def getEvent(id=""):
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    if id:
        event = Events.query.get(id)
    else:
        if not limit:
            limit = 100
        if not offset:
            offset = 0

        event = Events.query.offset(int(offset)).limit(int(limit)).all()
    print(event)
    rsp = Response(json.dumps(event, default=str), status=200, content_type="application/json")
    return rsp


@application.route("/Event", methods=["POST"])
def addEvent():
    body = json.loads(request.data.decode())
    try:
        if "type" in body:
            event = Events(subject=body['subject'], type=body.get('type'), message=body['message'])
        else:
            event = Events(subject=body['subject'], message=body['message'])
        db.session.add(event)
        db.session.commit()
    except Exception as e:
        print('DB Error: ', e)
        rsp = Response("Error on event registration", status=401, content_type="text/plain")
        return rsp

    print(event)
    rsp = Response("Event registered", status=200, content_type="text/plain")
    return rsp


@application.route("/Event/id/<id>", methods=["DELETE"])
def deleteEvent(id):
    event = Events.query.get(id)
    db.session.delete(event)
    db.session.commit()
    print(event)
    rsp = Response(json.dumps(event, default=str), status=200, content_type="application/json")
    return rsp


@application.route("/Event/id/<id>", methods=["PUT"])
def updateEvent(id):
    body = json.loads(request.data.decode())
    try:
        event = Events.query.filter_by(id=id).update(
            dict(
                subject=body['subject'],
                type=body['type'],
                message=body['message'],
            )
        )
        db.session.commit()
        if not event:
            print("id does not exist")
            rsp = Response("id does not exist", status=401, content_type="text/plain")
            return rsp
    except Exception as e:
        print("Error on update:", e)
        rsp = Response("Error on event update", status=401, content_type="text/plain")
        return rsp

    print("event updated")
    rsp = Response("Event updated", status=200, content_type="text/plain")
    return rsp
