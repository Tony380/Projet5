from program import Program


def main():
    program = Program()
    while True:
        try:
            print("\n---MAIN MENU---\n"
                  "1 - Which product would you like to replace?\n"
                  "2 - Check my substitute products\n"
                  "0 - Quit")
            choice = int(input("\nEnter your choice : "))

            if choice == 1:
                while True:
                    program.display_categories()
                    try:
                        program.cat_id = int(input("\nChoose a category : "))
                        if 1 <= program.cat_id <= 10:
                            break
                        else:
                            print("\nUNAVAILABLE CHOICE!")

                    except ValueError:
                        print("\nUNAVAILABLE CHOICE!")

                while True:
                    program.display_products()
                    try:
                        program.prod_id = int(input("\nChoose a product : "))
                        if program.prod_id in program.prod_list:
                            break
                        else:
                            print("\nUNAVAILABLE CHOICE!")
                    except ValueError:
                        print("\nUNAVAILABLE CHOICE!")

                while True:
                    try:
                        program.display_product()
                        program.display_substitute()
                        print("\n1 - Save this substitute\n"
                              "2 - Main menu\n"
                              "0 - Quit\n")
                        choice = int(input("Enter your choice : "))
                        if choice == 1:
                            program.save_substitute()
                            break
                        elif choice == 2:
                            break
                        elif choice == 0:
                            program.disconnect()
                        else:
                            print("\nUNAVAILABLE CHOICE!")

                    except ValueError:
                        print("\nUNAVAILABLE CHOICE!")

            elif choice == 2:
                program.is_saved()
                if len(program.fav_list) == 0:
                    print("You do not have any saved products")
                elif len(program.fav_list) > 0:
                    program.display_saved()

            elif choice == 0:
                program.disconnect()

            else:
                print("\nUNAVAILABLE CHOICE!")

        except ValueError:
            print("\nUNAVAILABLE CHOICE!")


main()
