import re

CONTACTS_FILE = "contacts.txt"

def load_contacts():
    contacts = []
    try:
        with open(CONTACTS_FILE, "r") as file:
            lines = file.readlines()[2:]
            for line in lines:
                parts = line.strip().split(" | ")
                if len(parts) == 4:
                    _,name, phone, email = parts
                    contacts.append({"name": name, "phone": phone, "email": email})
    except FileNotFoundError:
        pass
    return contacts

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        file.write("{:<5} | {:<20} | {:<15} | {:<25}\n".format("No.", "Name", "Phone", "Email"))
        file.write("-" * 75 + "\n")  
        for idx, contact in enumerate(contacts, 1):
            file.write("{:<5} | {:<20} | {:<15} | {:<25}\n".format(
                idx, contact['name'], contact['phone'], contact['email']))
            
def is_unique(field, value, contacts, current_index=None):
    for idx, contact in enumerate(contacts):
        if idx == current_index:
            continue
        if contact[field] == value:
            return False
    return True

def input_contact_fields(contacts, existing=None, current_index=None):
    
    while True:
        name = input(f"Enter Name {existing['name'] if existing else ''}: ").strip()
        if not name and existing:
            name = existing['name']
        else:
            name = name.title()
            if not re.fullmatch(r"[A-Z][a-z]*([ ][A-Z][a-z]*)*", name):
                print("Something Wrong!!Invalid name.\nUse only letters.")
                continue

        while True:
            phone = input(f"Enter Mobile Number {existing['phone'] if existing else ''}: ").strip()
            if not phone and existing:
                phone = existing['phone']
                break
            if not phone.isdigit() or len(phone) != 10:
                print("Something wrong!!Invalid phone number.\nEnter exactly 10 digits.")
                continue
            if not is_unique("phone", phone, contacts, current_index):
                print("This phone number already exists.")
                continue
            break

        while True:
            email = input(f"Enter Email Address {existing['email'] if existing else ''}: ").strip()
            if not email and existing:
                email = existing['email']
                break
            if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
                print("Something wrong!!Invalid email format.\nMust be a valid Gmail address(example@gmail.com).")
                continue
            if not is_unique("email", email, contacts, current_index):
                print("This email ID already exists.")
                continue
            break

        return {"name": name, "phone": phone, "email": email}

def add_contact(contacts):
    contact = input_contact_fields(contacts)
    contacts.append(contact)
    save_contacts(contacts)
    print("Contact Added Successfully!")

def view_contacts(contacts):
    if not contacts:
        print("No contacts Present")
        return
    print("\n*** Contact List ***")
    print("{:<5} {:<20} {:<15} {:<25}".format("No.", "Name", "Phone", "Email"))
    print("-" * 70)
    for i, contact in enumerate(contacts, 1):
        print("{:<5} {:<20} {:<15} {:<25}".format(i, contact['name'], contact['phone'], contact['email']))

def edit_contact(contacts):
    view_contacts(contacts)
    try:
        index = int(input("Enter Contact Serial Number To Edit: ")) - 1
        if 0 <= index < len(contacts):
            contacts[index] = input_contact_fields(contacts, existing=contacts[index], current_index=index)
            save_contacts(contacts)
            print("Contact Updated Successfully.")
        else:
            print("Invalid serial number.")
    except ValueError:
        print("Invalid input.")

def delete_contact(contacts):
    view_contacts(contacts)
    try:
        index = int(input("Enter Contact Serial Number To Delete: ")) - 1
        if 0 <= index < len(contacts):
            removed = contacts.pop(index)
            save_contacts(contacts)
            print(f"Deleted contact: {removed['name']}")
        else:
            print("Invalid serial number.")
    except ValueError:
        print("Invalid input.")

def main():
    contacts = load_contacts()
    options = {
        "1": add_contact,
        "2": view_contacts,
        "3": edit_contact,
        "4": delete_contact
    }

    while True:
        print("\n#### Contact Management System ####")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Edit Contact")
        print("4. Delete Contact")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice in options:
            options[choice](contacts)
        elif choice == "5":
            save_contacts(contacts)
            print("Exited Successfully")
            break
        else:
            print("Invalid Choice!!")

if __name__ == "__main__":
    main()