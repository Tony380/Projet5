"""This is the main program file"""
from purbeurre import Purbeurre


def main():
    # creating our database object
    purbeurre = Purbeurre()
    purbeurre.db_creation()
    purbeurre.db_fill()
    while True:
        try:
            print("\n---MAIN MENU---\n"
                  "1 - Which product would you like to replace?\n"
                  "2 - Check my substitute products\n"
                  "0 - Quit the program")
            choice = int(input("\nEnter your choice : "))

            if choice == 1:
                while True:
                    print("\n---CATEGORIES---")
                    purbeurre.display_categories()
                    try:
                        purbeurre.cat_id = int(input("\nChoose a category : "))
                        # avoid user to type a category that doesn't exit
                        if 1 <= purbeurre.cat_id <= 10:
                            break
                        else:
                            print("\nUNAVAILABLE CHOICE!")

                    except ValueError:
                        print("\nUNAVAILABLE CHOICE!")

                while True:
                    print("\n---PRODUCTS---")
                    purbeurre.display_products()
                    try:
                        purbeurre.prod_id = int(input("\nChoose a product : "))
                        # avoid user to type a product that is not available in this category
                        if purbeurre.prod_id in purbeurre.prod_list:
                            break
                        else:
                            print("\nUNAVAILABLE CHOICE!")
                    except ValueError:
                        print("\nUNAVAILABLE CHOICE!")

                while True:
                    try:
                        purbeurre.display_product()
                        purbeurre.display_substitute()
                        print("\n1 - Save this substitute\n"
                              "2 - Main menu\n"
                              "0 - Quit the program\n")
                        choice = int(input("Enter your choice : "))
                        if choice == 1:
                            purbeurre.save_substitute()
                            break
                        elif choice == 2:
                            break
                        elif choice == 0:
                            purbeurre.disconnect()
                        else:
                            print("\nUNAVAILABLE CHOICE!")

                    except ValueError:
                        print("\nUNAVAILABLE CHOICE!")

            elif choice == 2:
                purbeurre.is_saved()
                if len(purbeurre.fav_list) == 0:
                    print("You do not have any saved products")
                elif len(purbeurre.fav_list) > 0:
                    purbeurre.display_saved()

            elif choice == 0:
                purbeurre.disconnect()

            else:
                print("\nUNAVAILABLE CHOICE!")

        except ValueError:
            print("\nUNAVAILABLE CHOICE!")


if __name__ == "__main__":
    main()
