from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required."}), 400

    new_id = max((event.id for event in events), default=0) + 1
    new_event = Event(new_id, title.strip())
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update an event title
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": f"Event with id {id} not found."}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required."}), 400

    event.title = title.strip()

    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": f"Event with id {id} not found."}), 404

    events.remove(event)

    return jsonify({
        "message": f"Event with id {id} deleted successfully."
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
