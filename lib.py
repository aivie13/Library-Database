import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from datetime import date

def initialize_firestore():
    """
    Create database connection
    """
    # Setup Google Cloud Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cs246-library-firebase-adminsdk-mdxow-ba3bb9c0e8.json"

    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'cs246-library',
    })

    # Get reference to database
    db = firestore.client()
    return db

def display_library(db):
    """
    Display all Appointments for a tutor
    """
    # Query based on the tutor name only
    results = db.collection("Books").get()
    print()
    print("Books in the Library")
    print("{:<20}  {:<10}".format("Name", "Status"))
    for result in results:
        appt = result.to_dict()
        print("{:<20}  {:<10}".format(appt["title"], appt["status"]))
    print()   

def add_book(db):
    name = input('Enter book title: ')
    print()
    data = {
        'date': '', 'status':'available', 'title': name, 'userID': ''
    }
    db.collection('Books').document(name).set(data)

def check_out(db):
    print('What book would you like to check out?')
    book = input('> ')

    result = db.collection('Books').document(book).get()
    if result.exists:
        print('Please enter your name')
        userID = input('> ')
        book_data = {
            'date': str(date.today()), 'userID': userID
        }
        db.collection('Books').document(book).update(book_data)
    else:
        print('Sorry, it looks like we don\'t have that book on hand.')

def return_book(db):
    print('What book would you like to return')
    book = input('> ')

    result = db.collection('Books').document(book).get()
    if result.exists:
        book_data = {
            'date': '', 'userID': '', 'status': 'available'
        }
        db.collection('Books').document(book).update(book_data)
    else:
        print('Sorry, it looks like that book doesn\'t exist in the library.')

def remove_book(db):
    print('Which book would you like to remove?')
    book = input('> ')
    result = db.collection('Books').document(book).get()
    if result.exists:
        db.collection('Books').document(book).delete
    else:
        print('Sorry, it looks like that book doesn\'t exist in the library.')

def list_unavailable(db):
    print('Enter the name you gave at checkout')
    name = input('> ')
    print()
    query = db.collection("Books").where("userID","==",name)
    results = query.get()
    print("{:<20}  {:<10}".format("Name", "Date CHecked Out"))
    for result in results:
        arr = result.to_dict()
        print("{:<20}  {:<10}".format(arr["title"], arr["date"]))
    print()   
    

def menu(db):
    end = False
    while not end:
        print('1) List Library')
        print('2) Check Out Book')
        print('3) Return Book')
        print('4) Add Book')
        print('5) Remove Book')
        print('6) List books I\'ve checked out')
        print('Q) Quit')
        command = input('> ')
        if command == '1':
            display_library(db)

        elif command == '2':
            check_out(db)

        elif command == '3':
            return_book(db)

        elif command == '4':
            add_book(db)

        elif command == '5':
            remove_book(db)

        elif command == '6':
            list_unavailable(db)

        elif command == 'Q':
            end = True
        elif command == 'q':
            end = True

def main():

    db = initialize_firestore()
    menu(db)

if __name__ == "__main__":
    main()