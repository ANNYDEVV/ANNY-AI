from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community_engagement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class UserEngagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    interactions = db.Column(db.Integer, default=0)
    last_interaction = db.Column(db.Float, default=time.time)

class CommunityEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    timestamp = db.Column(db.Float, default=time.time)

db.create_all()

@app.route('/engage', methods=['POST'])
def engage():
    try:
        data = request.json
        username = data['username']

        user = UserEngagement.query.filter_by(username=username).first()
        if not user:
            user = UserEngagement(username=username, interactions=1, last_interaction=time.time())
        else:
            user.interactions += 1
            user.last_interaction = time.time()

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Engagement recorded", "username": username, "interactions": user.interactions}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400

@app.route('/community_event', methods=['POST'])
def create_event():
    try:
        data = request.json
        event_name = data['event_name']
        description = data.get('description', "")

        event = CommunityEvent(event_name=event_name, description=description)
        db.session.add(event)
        db.session.commit()

        return jsonify({"message": "Event created successfully", "event_name": event_name}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400

@app.route('/events', methods=['GET'])
def list_events():
    events = CommunityEvent.query.order_by(CommunityEvent.timestamp.desc()).all()
    result = [{
        "event_name": event.event_name,
        "description": event.description,
        "timestamp": event.timestamp
    } for event in events]

    return jsonify(result), 200

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    users = UserEngagement.query.order_by(UserEngagement.interactions.desc()).all()
    result = [{
        "username": user.username,
        "interactions": user.interactions
    } for user in users]

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
