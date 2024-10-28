from flask import Blueprint, request, jsonify, render_template
from .database import get_db
import re
import geocoder

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()

    ip_addresses = db.execute('SELECT * FROM ip_addresses').fetchall()
    
    # Fetch threat actors
    threat_actors = db.execute('SELECT * FROM threat_actors').fetchall()
    
    return render_template('index.html', ip_addresses=ip_addresses, threat_actors=threat_actors)

@bp.route('/', methods=['POST'])
def my_form_post():
    ip = request.form.get('ip')  # Use get to avoid KeyError
    threat_actor_name = request.form.get('TA')  # Get the threat actor name

    print(f"IP: {ip}, Threat Actor: {threat_actor_name}")

    if not is_valid_ip(ip):
        return jsonify({'error': 'Invalid IP address'}), 400

    # Add IP address to the database
    add_ip(ip)

    # If a threat actor name is provided, add it to the database
    if threat_actor_name:
        add_threat_actor(ip, threat_actor_name)

    return jsonify({'message': 'IP added successfully'}), 201 


def add_ip(ip):
    geo_ip = geocoder.ip(ip)

    db = get_db()
    db.execute('INSERT INTO ip_addresses (ip, country, city) VALUES (?, ?, ?)', (ip, str(geo_ip.country), str(geo_ip.city)))
    db.commit()

    return jsonify({'message': 'IP added successfully'}), 201


def add_threat_actor(ip, threat_actor_name):
    db = get_db()
    db.execute('INSERT INTO threat_actors (ip, threat_actor_name) VALUES (?, ?)', (ip, threat_actor_name))
    db.commit()

    return jsonify({'message': 'Threat actor added successfully'}), 201


def is_valid_ip(ip):
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
              r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
              r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
              r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(pattern, ip) is not None

