"""This class represents categories"""
from purbeurre import Purbeurre


class Category(Purbeurre):
    NAME = ["Muffins", "Steaks", "Biscuits", "Tortellini", "Viennoiseries",
            "Taboulés", "Confitures", "Cassoulets", "Yaourts", "Sodas"]

    def __init__(self):
        super().__init__()
        self.id = 0


    def fill_cat(self):
        self.cursor.execute("USE purbeurre")
        self.cursor.execute("SELECT COUNT(id) FROM Category")
        for answer in self.cursor:
            if answer[0] < len(self.NAME):
                for element in self.NAME:
                    self.id += 1
                    self.cursor.execute("INSERT INTO Category (name) VALUES ('{}')".format(element))
        self.my_db.commit()


    def display_categories(self):
        """Display the list of categories"""
        self.cursor.execute("SELECT * FROM Category ORDER BY id")
        for i in self.cursor.fetchall():
            print(i[0], "-", i[1])
