import mysql.connector
import requests
import config


class Program:
    def __init__(self):
        self.my_db = mysql.connector.connect(host=config.host, user=config.user, password=config.password)
        self.cursor = self.my_db.cursor()
        self.cat_id = int
        self.prod_id = int
        self.id = int
        self.prod_list = []
        self.fav_list = {}


    def db_creation(self):
        for line in open("database.sql").read().split(';\n'):
            self.cursor.execute(line)


    def db_fill(self):
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
                    self.my_db.commit()
                    for i in products:
                        if i.get("product_name", False) and i.get("brands", False) and \
                                i.get("nutrition_grades", False) and i.get("stores", False):
                            product = (i['product_name'], i['brands'], i['nutrition_grades'],
                                       i['stores'], cat_id, i['url'])
                            operation = "INSERT INTO Product (name, brand, nutriscore, store, cat_id, url)" \
                                        " VALUES (%s, %s, %s, %s, %s, %s) "
                            self.cursor.execute(operation, product)
                            self.my_db.commit()


    def disconnect(self):
        self.cursor = self.cursor.close()
        self.my_db = self.my_db.close()
        quit()


    def display_categories(self):
        self.cursor.execute("SELECT * FROM Category ORDER BY id")
        for i in self.cursor.fetchall():
            print(i[0], "-", i[1])


    def display_products(self):
        self.prod_list.clear()
        self.cursor.execute("SELECT id, name FROM Product WHERE cat_id ='{}'".format(self.cat_id))
        for result in self.cursor.fetchall():
            print(result[0], "-", result[1])
            self.prod_list.append(result[0])


    def display_product(self):
        self.cursor.execute("SELECT name, brand, nutriscore, store, url"
                            " FROM Product WHERE id ={}".format(self.prod_id))
        for i in self.cursor.fetchall():
            print("Product name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                  "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])


    def display_substitute(self):
        self.cursor.execute("SELECT name, brand, nutriscore, store, url, id FROM Product WHERE cat_id ={} "
                            "ORDER BY nutriscore LIMIT 1".format(self.cat_id))
        for i in self.cursor.fetchall():
            print("Product name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                  "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])
            self.id = i[5]


    def save_substitute(self):
        self.cursor.execute("INSERT INTO Substitute (sub_id, prod_id) VALUES ({}, {})".format(self.id, self.prod_id))
        self.my_db.commit()
        self.cursor.execute("SELECT sub_id, prod_id FROM Substitute")
        for i in self.cursor.fetchall():
            self.fav_list[i[0]] = "{}".format(i[1])


    def display_saved(self):
        self.my_db.commit()
        self.cursor.execute("SELECT Product1.name, Product1.url, Product2.name, Product2.url FROM SUBSTITUTE "
                            "INNER JOIN Product AS Product1 ON Substitute.sub_id = Product1.id "
                            "INNER JOIN Product AS Product2 ON Substitute.prod_id = Product2.id")
        for i in self.cursor.fetchall():
            print("Product name : {}".format(i[0]), "\n"
                  "Link to OpenFoodFacts :", i[1], "\n"
                  "Substitutes this product :\n"
                  "Product name : {}".format(i[2]), "\n"
                  "Link to OpenFoodFacts :", i[3], "\n")


    def is_saved(self):
        self.my_db.commit()
        self.cursor.execute("SELECT * FROM Substitute")
        for i in self.cursor.fetchall():
            self.fav_list[i[0]] = i[1]
