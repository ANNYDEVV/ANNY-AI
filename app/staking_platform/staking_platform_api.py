from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import time

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///staking_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Staker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(42), unique=True, nullable=False)
    staked_amount = db.Column(db.Float, default=0.0)
    rewards = db.Column(db.Float, default=0.0)
    last_stake_time = db.Column(db.Float, default=time.time)

db.create_all()

@app.route('/stake', methods=['POST'])
def stake():
    try:
        data = request.json
        address = data['address']
        amount = float(data['amount'])

        staker = Staker.query.filter_by(address=address).first()
        if not staker:
            staker = Staker(address=address, staked_amount=amount, last_stake_time=time.time())
        else:
            staker.staked_amount += amount
            staker.last_stake_time = time.time()

        db.session.add(staker)
        db.session.commit()
        return jsonify({"message": "Successfully staked", "address": address, "staked_amount": staker.staked_amount}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route('/unstake', methods=['POST'])
def unstake():
    try:
        data = request.json
        address = data['address']
        amount = float(data['amount'])

        staker = Staker.query.filter_by(address=address).first()
        if not staker or staker.staked_amount < amount:
            return jsonify({"error": "Insufficient staked balance"}), 400

        staker.staked_amount -= amount
        db.session.commit()
        return jsonify({"message": "Successfully unstaked", "address": address, "staked_amount": staker.staked_amount}), 200
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

    staker = Staker.query.filter_by(address=address).first()
    if not staker:
        return jsonify({"error": "Staker not found"}), 404

    return jsonify({"address": staker.address, "rewards": staker.rewards}), 200

@app.route('/distribute_rewards', methods=['POST'])
def distribute_rewards():
    try:
        data = request.json
        total_rewards = float(data['total_rewards'])

        stakers = Staker.query.all()
        total_staked = sum(staker.staked_amount for staker in stakers)

        if total_staked == 0:
            return jsonify({"error": "No staked tokens available"}), 400

        for staker in stakers:
            reward = (staker.staked_amount / total_staked) * total_rewards
            staker.rewards += reward

        db.session.commit()
        return jsonify({"message": "Rewards distributed successfully"}), 200
    except KeyError:
        return jsonify({"error": "Invalid payload"}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

@app.route('/stakers', methods=['GET'])
def list_stakers():
    stakers = Staker.query.all()
    result = [{
        "address": staker.address,
        "staked_amount": staker.staked_amount,
        "rewards": staker.rewards
    } for staker in stakers]

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
