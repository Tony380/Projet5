import mysql.connector
import requests


class Program:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.database = "purbeurre"
        self.my_db = mysql.connector.connect(host=self.host, database=self.database,
                                             user=self.user, password=self.password)
        self.cursor = self.my_db.cursor()
        self.cat_id = int
        self.prod_id = int
        self.url = ""
        self.prod_list = []
        self.fav_list = {}

    def fill_db(self):
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
                               "page_size": 200,
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
            self.url = i[4]

    def display_substitute(self):
        self.cursor.execute("SELECT name, brand, nutriscore, store, url"
                            " FROM Product WHERE cat_id ={} "
                            "ORDER BY nutriscore LIMIT 1".format(self.cat_id))

        for i in self.cursor.fetchall():
            print("Product name :", i[0] + "\n" + "Brand :", i[1] + "\n" + "Nutriscore :", i[2].upper() + "\n" +
                  "Stores :", i[3] + "\n" + "Link to OpenFoodFacts :", i[4])
            self.url = i[4]

    def save_favorite(self):
        self.cursor.execute("UPDATE Product SET favorite=1 WHERE url='{}'".format(self.url))
        self.my_db.commit()
        self.cursor.execute("SELECT id, name FROM Product WHERE url='{}'".format(self.url))
        for i in self.cursor.fetchall():
            self.fav_list[i[0]] = "{}".format(i[1])


    def display_favorite(self):
        self.my_db.commit()
        self.cursor.execute("SELECT id, name FROM Product WHERE favorite=1")
        for i in self.cursor.fetchall():
            print(i[0], "-", i[1])

    def erase_product(self):
        self.cursor.execute("UPDATE Product SET favorite=NULL WHERE id='{}'".format(self.prod_id))
        self.my_db.commit()
        self.fav_list.pop(self.prod_id)

    def is_favorite(self):
        self.my_db.commit()
        self.cursor.execute("SELECT id, name FROM Product WHERE favorite=1")
        for i in self.cursor.fetchall():
            self.fav_list[i[0]] = "{}".format(i[1])
