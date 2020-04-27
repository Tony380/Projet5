"""This class represents categories"""
from purbeurre import Purbeurre


class Category:
    LIST = ["Muffins", "Steaks", "Biscuits", "Tortellini", "Viennoiseries",
            "Taboulés", "Confitures", "Cassoulets", "Yaourts", "Sodas"]

    def __init__(self):
        self.id = 0
        self.purbeurre = Purbeurre()


    def fill_cat(self):
        self.purbeurre.cursor.execute("USE purbeurre")
        self.purbeurre.cursor.execute("SELECT COUNT(id) FROM Category")
        for answer in self.purbeurre.cursor:
            if answer[0] < len(self.LIST):
                for element in self.LIST:
                    self.id += 1
                    self.purbeurre.cursor.execute("INSERT INTO Category (name) VALUES ('{}')".format(element))
        self.purbeurre.my_db.commit()


    def display_categories(self):
        """Display the list of categories"""
        self.purbeurre.cursor.execute("USE purbeurre")
        self.purbeurre.cursor.execute("SELECT * FROM Category ORDER BY id")
        for i in self.purbeurre.cursor.fetchall():
            print(i[0], "-", i[1])
