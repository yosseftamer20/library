def account():
    j = open("members_account", "r")
    print("Open an account")
    id = 0
    last = j.readlines()
    if last:
        id = int(last[-1][0])
    id += 1
    j.close()
    name = input("name:")
    dob = input("dob:")
    telephone_number = input("telephone_number:")
    j = open("members_account", "a")
    if name.isalpha() and telephone_number.isdigit() and dob.isdigit():
        j.write(f"""{id},{name},{dob},{telephone_number}\n""")
        j.close()
    else:
        print("Invalid input")
def search_book():
    j = open("books.csv", "r")
    all_lines = j.readlines()
    name = input("enter book programming name or id:")
    for i, line in enumerate(all_lines):
        name_small = name.lower()
        line_small = line.lower()
        if name_small in line_small:
            print(line)
def checkout():
    j = open("books.csv", "r")
    all_lines = j.readlines()
    user_id = input("enter your id:")
    if user_id.isdigit():
        id = input("choice id you want:")
        found = None
        if id.isdigit():
            for i, line in enumerate(all_lines):
                s = line.split(",")
                if id == s[0] and "Available" == s[-1].strip():
                    found = True
                    print(line)
                    line = line.split(",")[:-1]
                    line.append("Borrowed" + "\n")
                    line = ",".join(line)
                    all_lines[i] = line
                    break
        if found:
                j = open("books.csv", "w")
                j.writelines(all_lines)
                j.close()
                j = open("members_account", "r")
                data = j.readlines()
                for i,h in enumerate(data):
                    lst = h.split(",")
                    lst[-1] = lst[-1].strip()
                    if user_id == lst[0]:
                        line = line.split(",")
                        lst.append(f"[{line[0]}]\n")
                        lst = ",".join(lst)
                        data[i] = lst
                j.close()
                j = open("members_account", "w")
                j.writelines(data)
                j.close()
        else:
            print("ID not found")
def return_book():
    j = open("books.csv", "r")
    all_lines = j.readlines()
    id = input("choice id you want:")
    found = None
    if id.isdigit():
        for i, line in enumerate(all_lines):
            s = line.split(",")
            if id == s[0] and "Borrowed" == s[-1].strip():
                found = True
                print(i, line)
                line = line.split(",")[:-1]
                line.append("Available" + "\n")
                line = ",".join(line)
                all_lines[i] = line
        if found:
            j = open("books.csv", "w")
            j.writelines(all_lines)
            j.close()
        else:
            print("ID not found")
while True:
    print("what you want \n1-create account.\n2-search book\n3-checkout book\n4-return book")
    choice = input("enter you choice:")
    if choice.isdigit():
        choice = int(choice)
        if choice == 1:
            account()
        elif choice == 2:
            search_book()
        elif choice == 3:
            checkout()
        elif choice == 4:
            return_book()
    else:
        print("Invalid Choice")