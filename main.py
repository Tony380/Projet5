from program import Program

main = Program()
main.fill_db()
main.is_favorite()
while True:
    try:
        print("\n---MAIN MENU---\n"
              "1 - Check categories\n"
              "2 - Favorite products\n"
              "0 - Quit")
        choice = int(input("\nEnter your choice : "))

        if choice == 1:
            while True:
                main.display_categories()
                try:
                    main.cat_id = int(input("\nChoose a category : "))
                    if 1 <= main.cat_id <= 10:
                        break
                    else:
                        print("\nUNAVAILABLE CHOICE!")

                except ValueError:
                    print("\nUNAVAILABLE CHOICE!")

            while True:
                main.display_products()
                try:
                    main.prod_id = int(input("\nChoose a product : "))
                    if main.prod_id in main.prod_list:
                        break
                    else:
                        print("\nUNAVAILABLE CHOICE!")
                except ValueError:
                    print("\nUNAVAILABLE CHOICE!")

            run = True
            while run:
                try:
                    main.display_product()
                    print("\n1 - Check for a healthier substitute product")
                    print("2 - Save this product")
                    print("3 - Main menu")
                    print("0 - Quit\n")
                    choice = int(input("Enter your choice : "))
                    if choice == 1:
                        while run:
                            try:
                                main.display_substitute()
                                print("\n1 - Save this product")
                                print("2 - Main menu")
                                print("0 - Quit\n")
                                choice = int(input("Enter your choice : "))
                                if choice == 1:
                                    main.save_favorite()
                                    run = False
                                elif choice == 2:
                                    run = False
                                elif choice == 0:
                                    main.disconnect()
                                else:
                                    print("\nUNAVAILABLE CHOICE!")
                            except ValueError:
                                print("\nUNAVAILABLE CHOICE!")

                    elif choice == 2:
                        main.save_favorite()
                        run = False
                    elif choice == 3:
                        break
                    elif choice == 0:
                        main.disconnect()
                    else:
                        print("\nUNAVAILABLE CHOICE!")
                except ValueError:
                    print("\nUNAVAILABLE CHOICE!")

        elif choice == 2:
            while True:
                try:
                    print("\n1 - Check your favorite products\n"
                          "2 - Erase a product\n"
                          "3 - Main menu\n"
                          "0 - Quit\n")
                    choice = int(input("Enter your choice : "))
                    if choice == 1:
                        if len(main.fav_list) == 0:
                            print("You have no favorite products")
                        elif len(main.fav_list) > 0:
                            main.display_favorite()
                    elif choice == 2:
                        if len(main.fav_list) == 0:
                            print("You have no favorite products")
                        elif len(main.fav_list) > 0:
                            while True:
                                main.display_favorite()
                                try:
                                    main.prod_id = int(input("\nWhich product do you want to erase? : \n"))
                                    main.erase_product()
                                    break
                                except ValueError:
                                    print("\nUNAVAILABLE CHOICE!\n")
                    elif choice == 3:
                        break
                    elif choice == 0:
                        quit()
                    else:
                        print("\nUNAVAILABLE CHOICE!")
                except ValueError:
                    print("\nUNAVAILABLE CHOICE!")

        elif choice == 0:
            main.disconnect()

        else:
            print("\nUNAVAILABLE CHOICE!")

    except ValueError:
        print("\nUNAVAILABLE CHOICE!")
