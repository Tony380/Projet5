"""This is the main program file"""
from purbeurre import Purbeurre
from category import Category
from product import Product


def main():
    """Our main program starts"""
    purbeurre = Purbeurre()
    purbeurre.db_creation()
    cat = Category()
    prod = Product()
    cat.fill_cat()
    prod.fill_prod()
    while True:
        try:
            print("\n---MENU PRINCIPAL---\n"
                  "1 - Quel aliment souhaitez-vous remplacer?\n"
                  "2 - Retrouver mes aliments substitués\n"
                  "0 - Quitter le programme")
            choice = int(input("\nEntrez votre choix : "))

            if choice == 1:
                while True:
                    print("\n---CATÉGORIES---")
                    cat.display_categories()
                    try:
                        prod.cat_id = int(input("\nSélectionnez la catégorie : "))
                        # avoid user to type a category that doesn't exit
                        if 1 <= prod.cat_id <= 10:
                            break
                        else:
                            print("\nCHOIX INVALIDE!")

                    except ValueError:
                        print("\nCHOIX INVALIDE!")

                while True:
                    print("\n---PRODUITS---")
                    prod.display_products()
                    try:
                        prod.id = int(input("\nSélectionnez un aliment : "))
                        # avoid user to type a product that is not available in this category
                        if prod.id in prod.prod_list:
                            break
                        else:
                            print("\nCHOIX INVALIDE!")
                    except ValueError:
                        print("\nCHOIX INVALIDE!")

                while True:
                    try:
                        prod.display_product()
                        prod.display_substitute()
                        print("\n1 - Enregistrer\n"
                              "2 - Menu principal\n"
                              "0 - Quitter le programme\n")
                        choice = int(input("Entrez votre choix : "))
                        if choice == 1:
                            prod.save_substitute()
                            break
                        elif choice == 2:
                            break
                        elif choice == 0:
                            purbeurre.disconnect()
                        else:
                            print("\nCHOIX INVALIDE!")

                    except ValueError:
                        print("\nCHOIX INVALIDE!")

            elif choice == 2:
                purbeurre.is_saved()
                if len(purbeurre.fav_list) == 0:
                    print("Vous n'avez aucun produit enregistré")
                elif len(purbeurre.fav_list) > 0:
                    purbeurre.display_saved()

            elif choice == 0:
                purbeurre.disconnect()

            else:
                print("\nCHOIX INVALIDE!")

        except ValueError:
            print("\nCHOIX INVALIDE!")


if __name__ == "__main__":
    main()
