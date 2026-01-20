from flask import Flask, request, jsonify
from tasks import long_running_job

app = Flask(__name__)

@app.route("/api/start-task", methods=["POST"])
def start_task():
    json = request.get_json()
    if json is None:
        return "Invalid input data", 400

    duration = json.get("duration")
    if duration is None:
        return "Missing duration parameter", 400


    result = long_running_job.delay(duration)
    return jsonify({
        "message": "Job received. Processing in background.",
        "task_id": result.id
    }), 202

@app.route("/api/status/<task_id>", methods=["GET"])
def get_task_status(task_id: str):
    task = long_running_job.AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Job is still processing...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result
        }
    else:
        # Handles FAILURE, RETRY, etc.
        response = {
            'state': task.state,
            'status': str(task.info)
        }

    return jsonify(response)