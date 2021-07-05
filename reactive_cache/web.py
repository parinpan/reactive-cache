import json
from reactive_cache.repository import Repository
from flask import Flask, Response, request, jsonify, render_template


class Dependency:
    def __init__(self):
        self.repo = None


dependency = Dependency()
app = Flask(__name__, template_folder="../templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/v1/profile/<username>", methods=["POST", "PUT", "PATCH"])
def update_profile(username):
    repo: Repository = dependency.repo
    action = request.args.get("action")

    if action not in ["inc_likes", "inc_followers", "inc_followings"]:
        return jsonify({"success": False}), 400

    try:
        repo.increase_counter(username, action)
    except:
        pass

    return jsonify({"success": True}), 200


@app.route("/stream")
def stream():
    username = request.args.get("username")

    def stream_profile():
        repo: Repository = dependency.repo
        prev_data = None

        while True:
            data = repo.get_profile_cache(username)

            if data != prev_data:
                prev_data = data
                yield "data: " + json.dumps(data) + "\n\n"

    return Response(stream_profile(), mimetype="text/event-stream")
