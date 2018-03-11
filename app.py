from trip_planner import BusTripPlanner
from flask import Flask, jsonify, request
from mcts import NoPlacesError

bus_trip_planner = BusTripPlanner()
app = Flask(__name__)



@app.route("/plan")
def plan():
    lat = float(request.args.get('lat', None))
    lon = float(request.args.get('lon', None))
    departure_time = int(request.args.get('departure_time', None))
    arrival_time = int(request.args.get('arrival_time', None))
    num_trips = int(request.args.get('num_trips', None))

    journeys = bus_trip_planner.plan((lat, lon), departure_time, arrival_time, 200, num_trips)
    results = [{
        "itinerary" : journey,
        "score" : score
    } for score, journey in journeys]
    return jsonify(results)

@app.errorhandler(NoPlacesError)
def bad_request_error(error):
    response = jsonify({"error" : error.msg})
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=False)