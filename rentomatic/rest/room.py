import json

from flask import Blueprint, request, Response

from rentomatic.repository.mongorepo import MongoRepo
from rentomatic.request_objects.room_list_request_object import RoomListRequestObject
from rentomatic.response_objects.response_objects import ResponseSuccess, ResponseFailure
from rentomatic.serializers import room_json_serializer as ser
from rentomatic.use_cases import room_list_use_case as uc

blueprint = Blueprint('room', __name__)

STATUS_CODES = {
    ResponseSuccess.SUCCESS: 200,
    ResponseFailure.RESOURCE_ERROR: 404,
    ResponseFailure.PARAMETERS_ERROR: 400,
    ResponseFailure.SYSTEM_ERROR: 500
}

connection_data = {
    'dbname': 'rentomaticdb',
    'user': 'root',
    'password': 'rentomaticdb',
    'host': 'localhost'
}


@blueprint.route('/rooms', methods=['GET'])
def room():
    repo = MongoRepo(connection_data)
    use_case = uc.RoomListUseCase(repo)

    query_str_params = {
        'filters': {},
    }

    for arg, values in request.args.items():
        if arg.startswith('filter_'):
            query_str_params['filters'][arg.replace('filter_', '')] = values

    request_object = RoomListRequestObject.from_dict(query_str_params)
    response = use_case.execute(request_object)

    return Response(json.dumps(response.value, cls=ser.RoomJsonEncoder),
                    mimetype='application/json', status=STATUS_CODES[response.type])
