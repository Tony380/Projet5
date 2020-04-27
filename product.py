"""This class contains the class Product. This class represents Product table in the database and fills it"""
import requests
from purbeurre import Purbeurre
from category import Category


class Product:
    def __init__(self):
        self.name = "product_name"
        self.brand = "brands"
        self.nutriscore = "nutrition_grades"
        self.store = "stores"
        self.cat_id = 0
        self.url = "url"
        self.purbeurre = Purbeurre()


    def fill_prod(self):
        self.purbeurre.cursor.execute("USE purbeurre")
        self.purbeurre.cursor.execute("SELECT COUNT(id) FROM Product")
        for answer in self.purbeurre.cursor:
            if answer[0] == 0:
                for element in Category.NAME:
                    payload = {"search_terms": "{}".format(element),
                               "page_size": 20,
                               "json": 1}
                    res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
                    result = res.json()
                    products = result["products"]
                    self.cat_id += 1
                    for i in products:
                        # avoid products with missing data
                        if i.get(self.name, False) and i.get(self.brand, False) and \
                                i.get(self.nutriscore, False) and i.get(self.store, False):
                            product = (i[self.name], i[self.brand], i[self.nutriscore],
                                       i[self.store], self.cat_id, i[self.url])
                            operation = "INSERT INTO Product (name, brand, nutriscore, store, cat_id, url)" \
                                        " VALUES (%s, %s, %s, %s, %s, %s) "
                            self.purbeurre.cursor.execute(operation, product)
        self.purbeurre.my_db.commit()
