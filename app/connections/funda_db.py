import sqlalchemy
import datetime as dt
from singleton_decorator import singleton
from typing import Optional
import os

from connections.util import query


@singleton
class FundaDB:
    def __init__(self):
        user = os.environ['FUNDA_DB_USER']
        password = os.environ['FUNDA_DB_PW']
        host = os.environ['FUNDA_DB_HOST']
        db = os.environ['FUNDA_DB_NAME']

        self.engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db}')

    @query
    def insert_house_data(self, link: str, city: str, house_surface: int, garden_surface: int,
                          rooms: int, price: int) -> None:
        sql = sqlalchemy.text('''
            INSERT INTO city_info
            VALUES (:link, :time_added, :city, :house_surface, :garden_surface, :rooms, :price)
        ''')
        sql = sql.bindparams(link=link, time_added=dt.datetime.now(), city=city,
                             house_surface=house_surface, garden_surface=garden_surface, rooms=rooms, price=price)
        self.engine.execute(sql)

    @query
    def get_house_rows(self, lower_price: Optional[float] = None, upper_price: Optional[float] = None):
        text = 'SELECT * FROM city_info'

        if lower_price and upper_price:
            text = text + f' WHERE {lower_price} < price < {upper_price}'
        elif lower_price:
            text = text + f' WHERE {lower_price} < price'
        elif upper_price:
            text = text + f' WHERE price < {upper_price}'

        sql = sqlalchemy.text(text)
        return self.engine.execute(sql)

    @query
    def insert_new_user(self, username: str, hashed_password: str) -> None:
        """Try to insert a new user into the database."""
        sql = sqlalchemy.text('''
            INSERT INTO users (username, user_password)
            VALUES (:username, :password);
        ''')
        sql = sql.bindparams(username=username, password=hashed_password)
        self.engine.execute(sql)

    @query
    def get_user_info(self, username: str):
        """Get user info for trying to log in."""
        sql = sqlalchemy.text(f'''
            SELECT username, user_password 
            FROM users 
            WHERE username = :username;
        ''')
        sql = sql.bindparams(username=username)
        result = self.engine.execute(sql).fetchone()
        result = {'username': result['username'], 'password': result['user_password']}
        return result
