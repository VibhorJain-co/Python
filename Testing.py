def DateEntry():
    date=''
    while True:
        i=1
        try:
            date = input("date of travel (dd/mm/yy): ")
            if len(date) != 8:
                raise ValueError

            for char in date:
                if i%3!=0:
                    int(char)
                    print("2 ")
                    i+=1
                elif char == '/':
                    i+=1
                    print("1")
                else:
                    raise ValueError

            else:
                break
        except ValueError:
            print("Please enter a Valid Date: \n")

    return date