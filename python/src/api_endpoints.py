import logging
import asyncio
import json

from flask import Blueprint, Response, request

# from utils.config import POD_NAME
# from utils.logging import is_ready_gauge, last_updated_gauge, job_start_counter, job_complete_counter, job_duration_summary
from websocket import send_message
from sqliteClient import NoteDB

logger = logging.getLogger(__name__)
api_endpoints = Blueprint('api', __name__)
notedb = NoteDB('notes.db')

# NB: uncomment code in main.py to enable these endpoints
# Any endpoints added here will be available at /api/<endpoint> - e.g. http://127.0.0.1:3000/api/example
# Change the the example below to suit your needs + add more as needed


@api_endpoints.route('/push', methods=['POST'])
def push():
    if request.headers.get('Content-Type') == 'application/json':
        # Parse JSON payload
        try:
            payload = request.get_json()
        except Exception as e:
            logger.error(f'Pushed data not in JSON: {payload}')
            return Response(f'Error parsing JSON: {e}', status=400)

        # Insert data to DB
        try:
            notedb.insert(payload.get('email'), payload.get('data'))
        except Exception as e:
            logger.error(f'Error storing data: {e}')
            return Response(f'Error storing data: {e}', status=500)

        # Send data to websocket
        try:
            asyncio.run(send_message(payload.get('data')))
        except Exception as e:
            logger.error(f'Error sending message: {e}')
            return Response(f'Error sending message: {e}', status=500)

        # Log and return
        logger.info(f'Pushed data: {payload}')
        return Response('Data received', status=200)

    else:
        return Response('Content-Type must be application/json', status=400)


@api_endpoints.route('/get', methods=['GET'])
def get():
    try:
        # Fetch and zip data
        data = notedb.fetch_all()
        column_names = [desc[0] for desc in notedb.client.cursor.description]
        data = [dict(zip(column_names, row)) for row in data]

    except Exception as e:
        logger.error(f'Error fetching data: {e}')
        return Response(f'Error fetching data: {e}', status=500)

    # Log and return
    return Response(json.dumps(data).encode('utf-8'), status=200, mimetype='application/json')


@api_endpoints.route('/clear', methods=['DELETE'])
def clear():
    try:
        notedb.delete_all()
    except Exception as e:
        logger.error(f'Error clearing data: {e}')
        return Response(f'Error clearing data: {e}', status=500)

    return Response('Data cleared', status=200)


@api_endpoints.route('/delete', methods=['DELETE'])
def delete():
    if 'id' not in request.args:
        return Response('ID parameter required', status=400)
    try:
        notedb.delete_single(request.args.get('id'))
    except Exception as e:
        logger.error(f'Error deleting data: {e}')
        return Response(f'Error deleting data: {e}', status=500)

    return Response('Data deleted', status=200)