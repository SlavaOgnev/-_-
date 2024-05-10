from peewee import *
import datetime

db = SqliteDatabase("pizza.db")


class User(Model):
    login = CharField(unique=True)
    password = CharField()
    order_count = IntegerField(default=0)

    class Meta:
        database = db


class Order(Model):
    id = AutoField(primary_key=True)
    price = IntegerField()
    date = CharField()
    user = ForeignKeyField(User, backref="orders")

    class Meta:
        database = db


db.create_tables([User, Order])
try:
    user_admin = User.create(login="admin", password="admin")
except IntegrityError:
    pass


def user_exists(login):
    try:
        User.get(User.login == login)
        return True
    except User.DoesNotExist:
        return False


def get_user(login):
    user = User.get(User.login == login)
    return user


def create_user(login, password):
    user = User.create(login=login, password=password)
    return user


def create_order(price, user):
    order = Order.create(price=price, user=user, date=datetime.date.today().strftime("%d.%m.%Y"))
    user.order_count += 1
    user.save()
    return order


def order_history(current_user):
    orders = current_user.orders
    return orders


db.close()
