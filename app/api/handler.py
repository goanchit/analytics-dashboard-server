from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
import json
from app.utils.validator import UserPostSchemaValidator
from app.actions.user import UserActions
from app.actions.base import BaseActions
import datetime
from app.utils.helper import handle_time

router = Blueprint('handler', __name__)

@router.get("/health")
def health_check():
    return "Service is up and running", 200

@router.get("/")
def create_user_logs():
    data = request.data
    data = json.loads(data)

    schema = UserPostSchemaValidator()

    try:
        schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user_id = data.get("user_id", None)
    UserActions.add_logs(
        request_data=request.data,
        user_id=user_id
    )
    return "Hello World", 200

@router.get("/logs")
def get_paginated_logs():
    from_ts = request.args.get('from_ts', default = datetime.datetime.now(tz=datetime.timezone.utc))
    to_ts = request.args.get('to_ts', default = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1))
    page_no = request.args.get('page_no', default= 0)

    from_ts, to_ts = handle_time(from_ts=from_ts, to_ts=to_ts)

    result = BaseActions.get_paginated_data(
        from_ts=from_ts,
        to_ts=to_ts,
        page_no=int(page_no)
    )
    return jsonify(result), 200

@router.get("/data")
def get_logs_data():
    from_ts = request.args.get('from_ts', default = datetime.datetime.now(tz=datetime.timezone.utc))
    to_ts = request.args.get('to_ts', default = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=1))

    from_ts, to_ts = handle_time(from_ts=from_ts, to_ts=to_ts)

    result = BaseActions.get_insights(
        from_ts=from_ts,
        to_ts=to_ts
    )
    return jsonify(result), 200

@router.post("/create-index")
def create_db_indexes():
    BaseActions.create_index()
    return jsonify("Created Index"), 200
