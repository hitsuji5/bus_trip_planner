from trip_planner import BusTripPlanner
from flask import Flask, jsonify, request
from error import NoPlacesError, BadRequestError

bus_trip_planner = BusTripPlanner()
app = Flask(__name__)



@app.route("/plan")
def plan():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        departure_time = int(request.args.get('departure_time'))
        arrival_time = int(request.args.get('arrival_time'))
        num_trips = int(request.args.get('num_trips'))
    except:
        raise BadRequestError

    journeys = bus_trip_planner.plan((lat, lon), departure_time, arrival_time, 200, num_trips)
    results = [{
        "itinerary" : journey,
        "score" : score
    } for score, journey in journeys]
    return jsonify(results)


@app.errorhandler(BadRequestError)
def bad_request_error(error):
    response = jsonify({"error" : error.msg})
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=False)