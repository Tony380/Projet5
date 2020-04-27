"""This file contains the class category. This class represents Category table in the database and fills it"""
from purbeurre import Purbeurre


class Category:
    NAME = ["Muffins", "Steaks", "Biscuits", "Tortellini", "Viennoiseries",
            "Taboulés", "Confitures", "Cassoulets", "Yaourts", "Sodas"]

    def __init__(self):
        self.id = 0
        self.purbeurre = Purbeurre()


    def fill_cat(self):
        self.purbeurre.cursor.execute("USE purbeurre")
        self.purbeurre.cursor.execute("SELECT COUNT(id) FROM Category")
        for answer in self.purbeurre.cursor:
            if answer[0] < len(self.NAME):
                for element in self.NAME:
                    self.id += 1
                    self.purbeurre.cursor.execute("INSERT INTO Category (name) VALUES ('{}')".format(element))
        self.purbeurre.my_db.commit()
