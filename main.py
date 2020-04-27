"""This is the main program file"""
from purbeurre import Purbeurre


def main():
    # creating our database object
    purbeurre = Purbeurre()
    purbeurre.db_creation()
    purbeurre.db_fill()
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
                    purbeurre.display_categories()
                    try:
                        purbeurre.cat_id = int(input("\nSélectionnez la catégorie : "))
                        # avoid user to type a category that doesn't exit
                        if 1 <= purbeurre.cat_id <= 10:
                            break
                        else:
                            print("\nCHOIX INVALIDE!")

                    except ValueError:
                        print("\nCHOIX INVALIDE!")

                while True:
                    print("\n---PRODUITS---")
                    purbeurre.display_products()
                    try:
                        purbeurre.prod_id = int(input("\nSélectionnez un aliment : "))
                        # avoid user to type a product that is not available in this category
                        if purbeurre.prod_id in purbeurre.prod_list:
                            break
                        else:
                            print("\nCHOIX INVALIDE!")
                    except ValueError:
                        print("\nCHOIX INVALIDE!")

                while True:
                    try:
                        purbeurre.display_product()
                        purbeurre.display_substitute()
                        print("\n1 - Enregistrer\n"
                              "2 - Menu principal\n"
                              "0 - Quitter le programme\n")
                        choice = int(input("Entrez votre choix : "))
                        if choice == 1:
                            purbeurre.save_substitute()
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
