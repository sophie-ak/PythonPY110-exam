# -*- coding: utf-8 -*-

from datetime import datetime as dt
import random
import sys

from faker import Faker

from conf import *
import simplejson as json


def check_length(limit):


    def actual_decorator(func):
        def wrapper():
            title = func()
            if len(title) > limit:
                raise ValueError(
                    "The title's length is greater " +
                    f"than the limit of {limit} chars.")
            return title
        return wrapper
    return actual_decorator


@check_length(limit=256)
def get_title(file_path: str='books.txt') -> str:
    with open(file_path, 'r') as f:
        return random.choice(f.readlines()).strip()


def get_year(min: int=1900, max: int=dt.now().year) -> int:
    return random.randint(min, max)


def get_page(min: int=1, max: int=sys.maxsize) -> int:
    return random.randint(min, max)


def get_isbn13() -> str:
    fake = Faker()
    return fake.isbn13()


def get_rating(ndigits: int=1) -> float:
    return round(random.uniform(1, 5), ndigits)


def get_price(min: int=1, max: int=sys.maxsize, ndigits: int=1) -> float:
    return round(random.uniform(min, max), ndigits)


def get_authors() -> list:
    fake = Faker()
    return [fake.name() for i in range(random.randint(1, 3))]


def books_generator(pk: int=1, max: int=100) -> list:
    while pk <= max:
        data = {
            "model": MODEL,
            "pk": pk,
            "fields": {
                "title": get_title(),
                "year": get_year(),
                "pages": get_page(max=1000),
                "isbn13": get_isbn13(),
                "rating": get_rating(),
                "price": get_price(max=100000),
                "author": get_authors()
            }
        }
        pk += 1
        yield data


def main():
    books = books_generator()
    with open('result.txt', 'w', encoding='utf8') as f:
        json.dump(books, f, indent=4, ensure_ascii=False,
                  iterable_as_array=True)


if __name__ == "__main__":
    main()
