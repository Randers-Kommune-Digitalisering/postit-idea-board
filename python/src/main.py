from flask import Flask
from healthcheck import HealthCheck
from prometheus_client import generate_latest

import asyncio
from utils.logging import set_logging_configuration, is_ready_gauge, last_updated_gauge
from utils.config import DEBUG, PORT, POD_NAME
from websocket import start_server
import threading
from api_endpoints import api_endpoints


set_logging_configuration()


def create_app():
    app = Flask(__name__)
    health = HealthCheck()
    app.add_url_rule('/healthz', 'healthcheck', view_func=lambda: health.run())
    app.add_url_rule('/metrics', 'metrics', view_func=generate_latest)

    app.register_blueprint(api_endpoints)  # Uncomment to add enpoints from api_endpoints.py

    @app.before_request
    def set_ready():
        is_ready_gauge.labels(job_name=POD_NAME, error_type=None).set(1)
        last_updated_gauge.set_to_current_time()
    
    return app


# Start server and websocket server in separate threads
def run_app():
    app = create_app()
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)

def run_ws_server():
    asyncio.run(start_server())

# Create threads for both functions
app_thread = threading.Thread(target=run_app)
ws_thread = threading.Thread(target=run_ws_server)

# Start both threads
app_thread.start()
ws_thread.start()

# Join both threads to the main thread to wait for their completion
app_thread.join()
ws_thread.join()

# if __name__ == '__main__':  # pragma: no cover
#     app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
