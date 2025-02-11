import requests
from haversine import haversine, Unit
from flask import Flask, jsonify, request

app = Flask(__name__)


def req_check(req):
    """
    Checks that each variable of the json payload is within the request
    and has the correct type

    Returns:
        message (string): message of the error or just a simple "ok"
        num (integer): endpoint
    """
    checklist = [
        'venue_slug',
        'cart_value',
        'user_lat',
        'user_lon'
    ]
    for query in checklist:
        if req.get(query) is None:
            return f'{query} not found in the get request', 400
    return 'ok', 200

def is_not_numerical(value, type):
    if type =="Float":
        try:
            float(value)
            return False
        except ValueError:
            return True
    else:
        try:
            float(value)
            return False
        except ValueError:
            return True

def get_req(domain):
    """
    GET request to the api and error checks it
    Returns:
        response (string or json object): either the json payload or an error message
        endpoint (integer): 200 or 400, depending on the type of domain
    """
    try:
        response = requests.get(domain)
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return f'Error making request: ${e}', 400


def find_range(ranges, distance):
    """
    finds the distance pricing "a" and "b" variables

    Returns:
        a (integer): venues "a" value for the delivery fee of a given distance
        b (integer): venues "b" value for the delivery fee of a given distance
    """
    for i in ranges:
        a = i['a']
        b = i['b']
        if distance <= i['max']:
            return a, b
    return None, None


def get_data(total_price, small_order_surcharge, cart_value, fee, distance):
    """
    changes the calculated variables into a ready json response payload

    Returns:
    total_price (integer): The calculated total price
    small_order_surcharge (integer): The calculated small order surcharge
    cart_value (integer): The cart value. This is the same as what was got as query parameter.
    delivery (object): An object containing:
        fee (integer): The calculated delivery fee
        distance (integer): The calculated delivery distance in meters
    """
    return {
        "total_price": total_price,
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": fee,
            "distance": distance
        }
    }


@app.route('/api/v1/delivery-order-price')
def calculate_cart():
    req = request.args
    message, num = req_check(req)
    if num == 400:
        return jsonify(message), 400
    venue = request.args.get('venue_slug')
    
    cart_value = request.args.get('cart_value')
    user_lat = request.args.get('user_lat')
    user_lon = request.args.get('user_lon')
    if is_not_numerical(cart_value, "Int"):
        return jsonify({'error': 'cart_value is not an int type:/'}), 400
    if is_not_numerical(user_lat, "Float"):
        return jsonify({'error': 'user_lat is not an int type:/'}), 400
    if is_not_numerical(user_lon, "Float"):
        return jsonify({'error': 'user_lon is not a float type:/'}), 400
    cart_value = int(cart_value)
    price = cart_value
    surcharge = 0
    # get the information from the designer venues api

    domain = 'https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/' + venue
    static_response, code_s = get_req(domain + '/static')
    dynamic_response, code_d = get_req(domain + '/dynamic')
    if code_s == 400:
        return jsonify({'error': 'the given venue_slug domain does not exists in the static API :/'}), 400
    if code_d == 400:
        return jsonify({'error': 'the given venue_slug domain does not exists in the dynamic API :/'}), 400

    # filter the json payload
    coordinates = static_response['venue_raw']['location']['coordinates']
    dynamic_specs = dynamic_response['venue_raw']['delivery_specs']
    base_price = dynamic_specs['delivery_pricing']['base_price']
    ranges = dynamic_specs['delivery_pricing']['distance_ranges']
    minimum = dynamic_specs['order_minimum_no_surcharge']

    # calculate the coordinate distance between two points of latitude and longitude using the haversine equation
    # (output in meters), it also rounds it to the closest 1 decimal

    distance = round(haversine((float(user_lat), float(user_lon)), (coordinates[1], coordinates[0]), unit=Unit.METERS),1)

    # check if the distance is within range of the venue => a and b are None is this is the case

    a, b = find_range(ranges, distance)
    if a is None:
        return {'error': 'the distance is too far for a delivery :('}, 400

    if cart_value < minimum:
        surcharge = minimum - cart_value
        price += surcharge

    delivery_price = base_price + a + b * distance / 10
    total_price = price + delivery_price
    data = get_data(total_price, surcharge, cart_value, delivery_price, distance)
    return jsonify(data), 200


@app.route('/')
def info():
    return 'Send hows it going the get request to "/api/v1/delivery-order-price" to calculate the wanted cart delivery', 400
