from sql_alchemy import database


class HotelModel(database.Model):
    __tablename__ = "hotels"

    hotel_id = database.Column(database.String, primary_key=True)
    title = database.Column(database.String(80))
    rate = database.Column(database.Float(precision=1))
    price = database.Column(database.Float(precision=2))
    city = database.Column(database.String(40))

    def __init__(self, hotel_id, title, rate, price, city):
        self.hotel_id = hotel_id
        self.title = title
        self.rate = rate
        self.price = price
        self.city = city

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "title": self.title,
            "rate": self.rate,
            "price": self.price,
            "city": self.city,
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        database.session.add(self)
        database.session.commit()

    def update_hotel(self, title, rate, price, city):
        self.title = title
        self.rate = rate
        self.price = price
        self.city = city

    def delete_hotel(self):
        database.session.delete(self)
        database.session.commit()
