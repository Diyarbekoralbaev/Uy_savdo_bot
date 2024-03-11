from aiogram.dispatcher.filters.state import StatesGroup, State

class Start(StatesGroup):
    phone = State()

class SellApartment(StatesGroup):
    type = State()
    photo = State()
    city = State()
    area = State()
    address = State()
    rooms = State()
    price = State()
    additional_info = State()
    check = State()

class Contact(StatesGroup):
    message = State()


class BuyApartment(StatesGroup):
    id = State()

class Subscription(StatesGroup):
    subscription = State()
    verification = State()
    photo = State()
