from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hotels(Resource):
    def get(self):
        return {"hotels": [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument(
        "title", type=str, required=True, help="The field 'title' cannot be left blank."
    )
    arguments.add_argument("rate")
    arguments.add_argument(
        "price",
        type=float,
        required=True,
        help="The field 'price' cannot be left blank.",
    )
    arguments.add_argument(
        "city", type=str, required=True, help="The field 'city' cannot be left blank."
    )

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found"}, 404

    @jwt_required
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400

        kwargs = Hotel.arguments.parse_args()
        hotel = HotelModel(hotel_id, **kwargs)
        try:
            hotel.save_hotel()
        except:
            return (
                {
                    "message": "An internal error ocurred while trying to save a new hotel."
                },
                500,
            )
        return hotel.json()

    @jwt_required
    def put(self, hotel_id):

        kwargs = Hotel.arguments.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.update_hotel(**kwargs)
            try:
                hotel.save_hotel()
            except:
                return (
                    {
                        "message": "An internal error ocurred while trying to save a new hotel."
                    },
                    500,
                )
            return hotel.json(), 200
        return {"message": "Hotel id '{}' does not exist.".format(hotel_id)}, 400

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return (
                    {
                        "message": "An internal error ocurred while trying to the delete a hote"
                    },
                    500,
                )
            return {"message": "Hotel deleted"}
        return {"message": "Hotel id '{}' not found.".format(hotel_id)}, 404
