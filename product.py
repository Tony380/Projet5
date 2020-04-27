"""This class represents products"""
import requests
from purbeurre import Purbeurre
from category import Category


class Product:
    def __init__(self):
        self.id = 0
        self.name = "product_name"
        self.brand = "brands"
        self.nutriscore = "nutrition_grades"
        self.store = "stores"
        self.cat_id = 0
        self.url = "url"
        self.purbeurre = Purbeurre()
        self.prod_list = []
        self.sub_id = 0


    def fill_prod(self):
        self.purbeurre.cursor.execute("USE purbeurre")
        self.purbeurre.cursor.execute("SELECT COUNT(id) FROM Product")
        for answer in self.purbeurre.cursor:
            if answer[0] == 0:
                for element in Category.LIST:
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


    def display_products(self):
        """Display the list of products"""
        self.prod_list.clear()
        self.purbeurre.cursor.execute("USE purbeurre")
        self.purbeurre.cursor.execute("SELECT id, name FROM Product WHERE cat_id ='{}'".format(self.cat_id))
        for result in self.purbeurre.cursor.fetchall():
            print(result[0], "-", result[1])
            self.prod_list.append(result[0])


    def display_product(self):
        """Display the chosen product"""
        self.purbeurre.cursor.execute("SELECT name, brand, nutriscore, store, url"
                                      " FROM Product WHERE id ={}".format(self.id))
        for i in self.purbeurre.cursor.fetchall():
            print("--------------------------------")
            print("Product name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                  "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])
            self.nutriscore = i[2]
            self.sub_id = self.id


    def display_substitute(self):
        """Display the chosen product's substitute"""
        self.purbeurre.cursor.execute("SELECT name, brand, nutriscore, store, url, id FROM Product WHERE cat_id = {} "
                                      "AND nutriscore = (SELECT MIN(nutriscore) FROM Product WHERE cat_id = {}) "
                                      "ORDER BY RAND() LIMIT 1".format(self.cat_id, self.cat_id))
        for i in self.purbeurre.cursor.fetchall():
            if i[2] != self.nutriscore:
                print("\nL'aliment suivant est un substitut plus sain :\n"
                      "\nProduct name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                      "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])
                print("--------------------------------")
                self.sub_id = i[5]
            else:
                print("\nIl n'y pas d'aliment plus sain disponible\n"
                      "--------------------------------")

    def save_substitute(self):
        """Save the substitute's id and the chosen product's id in the database"""
        self.purbeurre.cursor.execute("INSERT IGNORE INTO Substitute (sub_id, prod_id) "
                                      "VALUES ({}, {})".format(self.sub_id, self.id))
        self.purbeurre.my_db.commit()
        self.purbeurre.cursor.execute("SELECT sub_id, prod_id FROM Substitute")
        for i in self.purbeurre.cursor.fetchall():
            if i[0] not in self.purbeurre.fav_list:
                self.purbeurre.fav_list[i[0]] = "{}".format(i[1])
