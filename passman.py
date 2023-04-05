#!/usr/bin/python

from pmdbman import *
from pmcryptman import *
import os
import random
import string

menuMessage = '''
# WELCOME TO THE PASSMAN
# Please select an option:
---------------------------------------------
#1 Retrieve credentials
#2 Create new entry
#3 Update entry 
#4 Delete entry
#5 Exit Passman
---------------------------------------------
'''

def go_back():
    while True:
        goBack = input("Go back(Y/N): ")
        if goBack == 'Y' or goBack == 'y':
            return True
        elif goBack == 'n' or goBack == 'N':
            return False
        else:
            continue

def ui_clear():
    os.system('clear')

def show_all_entries():    
    db_showall()
        
        

def get_password():
    while True:
        try:
            show_all_entries()
            i = input("# Please enter the name of the site:")

            x = db_search(i)

            print("# The Username is " + x[0] + "\n# The Password is " + x[1])
        
            goBack = go_back()
            
            if goBack == True:
                break
            else:
                ui_clear()
        except TypeError:
            print("# Entry does not exist")
            break

def generate_password():
    letters = string.ascii_letters # all letters
    digits = string.digits # all digits
    special_chars = string.punctuation # all special characters
    
    password = []
    password.extend(random.choices(letters, k=8))
    password.extend(random.choices(digits, k=4))
    password.append(random.choice(special_chars))
    
    # shuffle password
    random.shuffle(password)
    
    # return as string
    return ''.join(password)

def make_a_entry():
    while True:
        
        i2 = input("# Please enter the site name:")
        i3 = input("# Please enter the Username:")
        choice = input("# Generate a random pw?(y/n):")
        if choice == "y":
            i4 = generate_password()
        elif choice == "n":
            i4 = input("# Please enter the password:")
        else:
            print("#Wrong input")
            continue
        db_insert(i2, i3, i4)

        print("# Account for " + str(i2) + " has been inserted!")

        goBack = go_back()
        if goBack == True:
            break
        else:
            ui_clear()

def update():
    while True:
        show_all_entries()
        i = input("# Please enter the name of the site:")
        i2 = input("# Please enter the new password:")

        db_update(i, i2)

        print("# Password has been updated for " + str(i))
        
        goBack = go_back()
        if goBack == True:
            break
        else:
            ui_clear()

def delete_entry():
    while True:
        show_all_entries()
        i = input("# Please enter the name of the entry you wish the remove:")
        db_delete(i)
        
        
        goBack = go_back()
        if goBack == True:
            break
        else:
            ui_clear()


def main():
    while True:
        try:
            #clear the terminal here
            ui_clear()
            print(menuMessage)

            option = int(input("#ENTER THE NUMBER OF YOUR SELECTION:"))
                
               
            if option == 1: #Get password
                #clear here
                ui_clear()
                
                get_password()
            
            elif option == 2: #Make an entry
                #clear here
                ui_clear()
                make_a_entry()

            elif option == 3: #Update the password for an entry
                #clear here
                ui_clear()
                update()

            elif option == 4: #delete an entry
                #clear here
                ui_clear()
                delete_entry()        

            elif option == 5: #exit
                #clear here
                ui_clear()
                break

            else:
                print("# INVALID INPUT")
        except ValueError:
                print("# VALUE ERROR!")


def passman_start():
    db_table_check()
    ks = db_get_ks()
    if ks is None:
        masterPassword = input("#Enter a new Master Password: ")
        db_insert_ks(masterPassword)
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

