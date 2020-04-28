"""This class represents our database 'Purbeurre'"""
import mysql.connector
import config


class Purbeurre:
    """Class Purbeurre directly connects to the database"""
    def __init__(self):
        self.my_db = mysql.connector.connect(host=config.host, user=config.user, password=config.password)
        self.cursor = self.my_db.cursor()
        self.fav_list = {}


    def db_creation(self):
        """Creates the database"""
        for line in open("database.sql").read().split(';\n'):
            self.cursor.execute(line)


    def disconnect(self):
        """Disconnection from the database"""
        self.cursor = self.cursor.close()
        self.my_db = self.my_db.close()
        print("\nAU REVOIR !")
        quit()


    def is_saved(self):
        """Checks if there are some saved products in the database and put them in a list"""
        self.fav_list.clear()
        self.my_db.commit()
        self.cursor.execute("SELECT * FROM Substitute")
        for i in self.cursor.fetchall():
            self.fav_list[i[0]] = i[1]


    def display_saved(self):
        """Displays substitute and chosen product"""
        self.cursor.execute("SELECT Product1.name, Product1.url, Product2.name, Product2.url FROM SUBSTITUTE "
                            "INNER JOIN Product AS Product1 ON Substitute.sub_id = Product1.id "
                            "INNER JOIN Product AS Product2 ON Substitute.prod_id = Product2.id")
        for i in self.cursor.fetchall():
            if i[1] == i[3]:
                print("\nNom du produit : {}".format(i[0]), "\n"
                      "Lien vers OpenFoodFacts :", i[1], "\n"
                      "Il n'y pas d'aliment plus sain disponible\n"
                      "--------------------------------")
            else:
                print("\nNom du produit : {}".format(i[0]), "\n"
                      "Lien vers OpenFoodFacts :", i[1], "\n"
                      "\nCe produit substitut le produit suivant :\n"
                      "\nNom du produit : {}".format(i[2]), "\n"
                      "Lien vers OpenFoodFacts :", i[3], "\n"
                      "--------------------------------")
