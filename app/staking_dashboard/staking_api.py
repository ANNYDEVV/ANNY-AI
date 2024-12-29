from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Flask app and database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///staking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(42), unique=True, nullable=False)
    staked_amount = db.Column(db.Float, default=0.0)
    rewards = db.Column(db.Float, default=0.0)

# Initialize database
db.create_all()

@app.route('/stake', methods=['POST'])
def stake_tokens():
    try:
        data = request.json
        address = data['address']
        amount = float(data['amount'])

        user = User.query.filter_by(address=address).first()
        if not user:
            user = User(address=address, staked_amount=amount)
        else:
            user.staked_amount += amount

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Staked successfully", "address": address, "staked_amount": user.staked_amount}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route('/unstake', methods=['POST'])
def unstake_tokens():
    try:
        data = request.json
        address = data['address']
        amount = float(data['amount'])

        user = User.query.filter_by(address=address).first()
        if not user or user.staked_amount < amount:
            return jsonify({"error": "Insufficient staked balance"}), 400

        user.staked_amount -= amount
        db.session.commit()
        return jsonify({"message": "Unstaked successfully", "address": address, "staked_amount": user.staked_amount}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route('/rewards', methods=['GET'])
def get_rewards():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400

    user = User.query.filter_by(address=address).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"address": user.address, "rewards": user.rewards}), 200

@app.route('/distribute_rewards', methods=['POST'])
def distribute_rewards():
    try:
        data = request.json
        total_rewards = float(data['total_rewards'])
        users = User.query.all()

        total_staked = sum(user.staked_amount for user in users)
        if total_staked == 0:
            return jsonify({"error": "No staked tokens available"}), 400

        for user in users:
            reward = (user.staked_amount / total_staked) * total_rewards
            user.rewards += reward

        db.session.commit()
        return jsonify({"message": "Rewards distributed successfully"}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
