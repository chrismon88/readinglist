""" 
Dan Smestad and Christian Montoya Project 2 Reading List.
Program to create and manages a list of books in a db that the user wishes to read. 
user can add remove list and check that the user has read or not read. 
"""


from bookstore import Book, BookStore
from menu import Menu
import ui
from bookstore import BookError

store = BookStore()

def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == 'Q' or choice == 'q':
            break

#adding option 7 to delete a book of choice.
def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Change Book Read Status', change_read)
    menu.add_option('7', 'Delete Book', delete_book)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_book():
    try:
        new_book = ui.get_book_info()
        new_book.save()
    except BookError: 
        print("\nThis book is already in the store.\n")


def delete_book():
    try:
        book_id_to_delete = ui.get_book_id()
        book = store.get_book_by_id(book_id_to_delete)
        if book:         
            book.delete()    
        else:
            ui.message('\nBook ID not found\n!')    

    except BookError:
        ui.message('\nError: book database error\n')
        

def show_read_books():
    read_books = store.get_books_by_read_value(True)
    ui.show_books(read_books)


def show_unread_books():
    unread_books = store.get_books_by_read_value(False)
    ui.show_books(unread_books)


def show_all_books():
    books = store.get_all_books()
    ui.show_books(books)


def search_book():
    search_term = ui.ask_question('Enter search term, will match partial authors or titles. ')
    matches = store.book_search(search_term)
    ui.show_books(matches)


## modified to check if the book is found or not before allowing modifification.
# Not None means book is found in database.
def change_read():
    book_id = ui.get_book_id()
    book = store.get_book_by_id(book_id)
    if book is not None:
        new_read = ui.get_read_value()     
        book.read = new_read
        ui.message(('You have read ' if book.read else 'You have not read ') + book.title + ' by author '+ book.author)      
        book.save()
    else:
        ui.message('\nBook ID enter was not found!\n')

    
def quit_program():
    ui.message('Thanks and bye!')


if __name__ == '__main__':
    main()
