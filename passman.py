#!/usr/bin/python

from pmdbman import *
from pmcryptman import *


menuMessage = '''
# WELCOME TO THE PASSMAN
# Please select an option:
---------------------------------------------
#1 Show all site entries
#2 Retrieve credentials
#3 Create new entry
#4 Update entry
#5 Delete entry
#6 Exit Passman
---------------------------------------------
'''





def go_back():
    goBack = input("Go back(Y/N): ")
    if goBack == 'Y' or goBack == 'y':
        return True
    elif goBack == 'n' or goBack == 'N':
        return False
    else:
        return True
    
def show_all_entries():
    while True:
        
        db_showall()
        
        goBack = go_back()
        if goBack == True:
            break


def get_password():
    while True:
        
        i = int(input("# Please enter the ID of the site:"))
        pw = db_show_password(i)
        #pull the key and salt
        #after the above has been changed to return the encrypted password, put it in a variable and decrypt it with key and salt, then print it
        print("The password is: " + str(pw))
        goBack = go_back()
        if goBack == True:
            break
#add function to decrypt the password from cryptman

def make_a_entry():
    while True:
        
        i = int(input("# Please enter the ID of the site:"))
        i2 = input("# Please enter the site name:")
        i3 = input("# Please enter the Username:")
        i4 = input("# Please enter the password:")
        #pulls the key and salt
        #encrypt i4 with the key and salt
        db_insert(i, i2, i3, i4)

        print("# Account for " + str(i2) + " has been inserted!")

        goBack = go_back()
        if goBack == True:
            break
#add Encryption method from cryptman

def update():
    while True:
        
        i = int(input("# Please enter the ID of the site:"))
        i2 = input("# Please enter the password:")

        db_update(i, i2)

        print("# Password has been updated for ID " + str(i))
        
        goBack = go_back()
        if goBack == True:
            break

def delete_entry():
    while True:
        
        i = int(input("# Please enter the ID of the entry you wish the remove:"))
        db_delete(i)
        print("# Successfully deleted!")
        
        goBack = go_back()
        if goBack == True:
            break


def main():
    while True:
        try:
            print(menuMessage)

            option = int(input("#ENTER THE NUMBER OF YOUR SELECTION:"))
                
            if option == 1:
                show_all_entries()

            elif option == 2: #Get password
                get_password()
            
            elif option == 3: #Make an entry
                make_a_entry()

            elif option == 4: #Update the password for an entry
                update()

            elif option == 5: #delete an entry
                delete_entry()        

            elif option == 6: #exit
                break

            else:
                print("# INVALID INPUT")
        except ValueError:
            print("# MUST ENTER AN INTEGER!")


def passman_start():
    db_table_check()
    ks = db_get_ks()
    if ks is None:
        masterPassword = input("#Enter a new Master Password: ")
        salt = input("#Enter a Salt: ")
        db_insert_ks(masterPassword, salt)
        print("#Key Created and stored!")
        main()    
    else:
        masterPassword = input("#Enter the master password:")
        pwattempt = create_key(masterPassword, ks[1])
        if pwattempt == ks[0]:
            print("#SUCCESS! STARTING PASSMAN!")
            main()
        else:
            print("#FAILURE CLOSING PASSMAN!")

passman_start()

