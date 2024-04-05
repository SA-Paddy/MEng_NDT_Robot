# Run a menu loop today
def men():

    print("\nMenu:")
    print("1. Only run a theoretical test model")
    print("2. Undertake analysis of a saved file")
    print("3. Continue with Script")
    print("4. Exit")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        print('running theoretical test only')
    elif choice == 2:
        print('running analysis module')
    elif choice == 3:
        print('running full test')
    elif choice == 4:
        print("Exiting the program.")
        exit()
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

    return choice

