"""This file contains the Program class and its methods"""
import mysql.connector
import requests
import config


class Purbeurre:
    """Class Purbeurre directly connects to the database"""
    def __init__(self):
        self.my_db = mysql.connector.connect(host=config.host, user=config.user, password=config.password)
        self.cursor = self.my_db.cursor()
        self.cat_id = int
        self.prod_id = int
        self.id = int
        self.score = ""
        self.prod_list = []
        self.fav_list = {}


    def db_creation(self):
        """Create the database"""
        for line in open("database.sql").read().split(';\n'):
            self.cursor.execute(line)


    def db_fill(self):
        """Fill the database from OpenFoodFacts"""
        categories = ["Muffins", "Steaks", "Biscuits", "Tortellini", "Viennoiseries", "Taboulés", "Confitures",
                      "Cassoulets", "Yaourts", "Sodas"]

        self.cursor.execute("SELECT COUNT(id) FROM Category")
        cat_id = 0
        for answer in self.cursor:
            if answer[0] < len(categories):
                for element in categories:
                    cat_id += 1
                    self.cursor.execute("INSERT INTO Category (name) VALUES ('{}')".format(element))
                    payload = {"search_terms": "{}".format(element),
                               "page_size": 50,
                               "json": 1}
                    res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
                    result = res.json()
                    products = result["products"]
                    for i in products:
                        # avoid products with missing data
                        if i.get("product_name", False) and i.get("brands", False) and \
                                i.get("nutrition_grades", False) and i.get("stores", False):
                            product = (i['product_name'], i['brands'], i['nutrition_grades'],
                                       i['stores'], cat_id, i['url'])
                            operation = "INSERT INTO Product (name, brand, nutriscore, store, cat_id, url)" \
                                        " VALUES (%s, %s, %s, %s, %s, %s) "
                            self.cursor.execute(operation, product)
                            self.my_db.commit()


    def disconnect(self):
        """Disconnection from the database"""
        self.cursor = self.cursor.close()
        self.my_db = self.my_db.close()
        print("\nGOOD BYE !")
        quit()


    def display_categories(self):
        """Display the list of categories"""
        self.cursor.execute("SELECT * FROM Category ORDER BY id")
        for i in self.cursor.fetchall():
            print(i[0], "-", i[1])


    def display_products(self):
        """Display the list of products"""
        self.prod_list.clear()
        self.cursor.execute("SELECT id, name FROM Product WHERE cat_id ='{}'".format(self.cat_id))
        for result in self.cursor.fetchall():
            print(result[0], "-", result[1])
            self.prod_list.append(result[0])


    def display_product(self):
        """Display the chosen product"""
        self.cursor.execute("SELECT name, brand, nutriscore, store, url"
                            " FROM Product WHERE id ={}".format(self.prod_id))
        for i in self.cursor.fetchall():
            print("--------------------------------")
            print("Product name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                  "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])
            self.score = i[2]
            self.id = self.prod_id


    def display_substitute(self):
        """Display the chosen product's substitute"""
        self.cursor.execute("SELECT name, brand, nutriscore, store, url, id FROM Product WHERE cat_id = {} AND "
                            "nutriscore = (SELECT MIN(nutriscore) FROM Product WHERE cat_id = {}) "
                            "ORDER BY RAND() LIMIT 1".format(self.cat_id, self.cat_id))
        for i in self.cursor.fetchall():
            if i[2] != self.score:
                print("\nThe following product is healthier :\n"
                      "\nProduct name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                      "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])
                print("--------------------------------")
                self.id = i[5]
            else:
                print("\nThere is no healthier alternative\n"
                      "--------------------------------")


    def save_substitute(self):
        """Save the substitute's id and the chosen product's id in the database"""
        self.cursor.execute("INSERT IGNORE INTO Substitute (sub_id, prod_id) "
                            "VALUES ({}, {})".format(self.id, self.prod_id))
        self.my_db.commit()
        self.cursor.execute("SELECT sub_id, prod_id FROM Substitute")
        for i in self.cursor.fetchall():
            if i[0] not in self.fav_list:
                self.fav_list[i[0]] = "{}".format(i[1])


    def display_saved(self):
        """Display substitute and chosen product"""
        self.cursor.execute("SELECT Product1.name, Product1.url, Product2.name, Product2.url FROM SUBSTITUTE "
                            "INNER JOIN Product AS Product1 ON Substitute.sub_id = Product1.id "
                            "INNER JOIN Product AS Product2 ON Substitute.prod_id = Product2.id")
        for i in self.cursor.fetchall():
            if i[1] == i[3]:
                print("\nProduct name : {}".format(i[0]), "\n"
                      "Link to OpenFoodFacts :", i[1], "\n"
                      "There is no healthier alternative\n"
                      "--------------------------------")
            else:
                print("\nProduct name : {}".format(i[0]), "\n"
                      "Link to OpenFoodFacts :", i[1], "\n"
                      "Substitutes this product :\n"
                      "Product name : {}".format(i[2]), "\n"
                      "Link to OpenFoodFacts :", i[3], "\n"
                      "--------------------------------")


    def is_saved(self):
        """Check if there are some saved products in the database and put them in a list"""
        self.fav_list.clear()
        self.my_db.commit()
        self.cursor.execute("SELECT * FROM Substitute")
        for i in self.cursor.fetchall():
            self.fav_list[i[0]] = i[1]
