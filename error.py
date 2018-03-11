
class BadRequestError(Exception):
    status_code= 400
    msg = "Request parameters are not well formatted"

class NoPlacesError(BadRequestError):
    msg = "Invalid initial location is provided."