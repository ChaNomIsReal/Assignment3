import abc
import datetime

class Member:
    def __init__(self, name, id, contact_info):
        self.name = name
        self.id = id
        self.contact_info = contact_info

    def display_details(self, member_id=None):
        if member_id is None or self.id == member_id:
            print("Name:", self.name)
            print("ID:", self.id)
            print("Contact Info:", self.contact_info)

class Publication(abc.ABC):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    @abc.abstractmethod
    def display_details(self):
        pass

class Book(Publication):
    def __init__(self, title, author, year, isbn, book_type):
        super().__init__(title, author, year)
        self.isbn = isbn
        self.book_type = book_type

    def display_details(self):
        print("Title:", self.title)
        print("Author:", self.author)
        print("Year:", self.year)
        print("ISBN:", self.isbn)
        print("Type:", self.book_type)

class Loan:
    def __init__(self, member, publication, loan_date):
        self.member = member
        self.publication = publication
        self.loan_date = loan_date
        self.due_date = loan_date + datetime.timedelta(days=14)  # Assume 14 days loan period

    def return_publication(self, publication, library):
        if self in library.loans:
            library.loans.remove(self)
            print("Publication", publication.title, "returned successfully")
            return True
        else:
            print("Failed to return publication")
            return False

    def display_loan_details(self):
        print("Member:", self.member.name)
        print("Publication:", self.publication.title)
        print("Loan Date:", self.loan_date.strftime("%Y-%m-%d"))
        print("Due Date:", self.due_date.strftime("%Y-%m-%d"))    

    def is_overdue(self):
        # Check if the loan is overdue
        return datetime.datetime.now() > self.due_date + datetime.timedelta(days=14)

class Library:
    def __init__(self):
        self.members = []
        self.publications = []
        self.loans = []

    def add_member(self, member):
        self.members.append(member)

    def search_member(self, member_id):
        for member in self.members:
            if member.id == member_id:
                return member  
        return None 

    def add_publication(self, publication):
        self.publications.append(publication)

    def search_publication(self, title=None, author=None, book_type=None):
        results = []
        for publication in self.publications:
            if (not title or publication.title == title) and \
               (not author or publication.author == author) and \
               (not book_type or isinstance(publication, Book) and publication.book_type == book_type):
                results.append(publication)
        return results

    def lend_publication(self, member, publication):
        # Check if the publication is available for loan
        if publication not in self.publications:
            print("Publication not found in library")
            return False
        # Check if the publication is already on loan
        for loan in self.loans:
            if loan.publication == publication:
                print("Publication already on loan")
                return False
        # Process loan
        loan_date = datetime.datetime.now()
        new_loan = Loan(member, publication, loan_date)
        self.loans.append(new_loan)
        print("Publication", publication.title, "lent to", member.name)
        return True

    def generate_overdue_loans_report(self):
        # Generate report of loans that are overdue
        overdue_loans = [loan for loan in self.loans if loan.is_overdue()]

        if not overdue_loans:
            print("No loans are currently overdue")
            return

        print("Overdue Loans Report:")
        for loan in overdue_loans:
            print("Publication:", loan.publication.title)
            print("Member:", loan.member.name)
            print("Due Date:", loan.due_date)
            print()

    def generate_popular_publications_report(self):
        # Generate report of popular publications
        if not self.loans:
            print("No loans have been made yet")
            return

        publication_counts = {}
        for loan in self.loans:
            publication_title = loan.publication.title
            if publication_title in publication_counts:
                publication_counts[publication_title] += 1
            else:
                publication_counts[publication_title] = 1

        popular_publications = sorted(publication_counts.items(), key=lambda x: x[1], reverse=True)

        print("Popular Publications Report:")
        for title, count in popular_publications:
            print("Title:", title)
            print("Number of Loans:", count)
            print()

def handle_member_management():
    print("\nMember Management")
    print("1. Add new member")
    print("2. Search for a member")
    print("3. Display member details")
    print("4. Exit Program")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        # Add Member
        name = str(input("Enter your Name: "))
        id = str(input("Enter your ID: "))
        contact_info = str(input("Enter your contact_info: "))
        NewMember = Member(name, id, contact_info)
        library.add_member(NewMember)
        handle_member_management()
    elif choice == 2:
        # Search for a member
        id = str(input("Enter ID: "))
        found_member = library.search_member(id)
        if found_member:
            print("Found Member")
        else:
            print("Member not found")
        handle_member_management()
    elif choice == 3:
        id = str(input("Enter ID want to Display: "))
        found_member = library.search_member(id)
        if found_member:
            found_member.display_details()
        else:
            print("Member not found")
        handle_member_management()

    elif choice == 4:
        UserInterface.display_menu()
        choice = int(input("Enter your choice: "))
        UserInterface.handle_menu_choice(choice)
    else:
        print("Invalid choice. Please select a valid option.")
        handle_member_management()
def handle_publication_management():
    print("\nPublication Management")
    print("1. Add new publication")
    print("2. Search for a publication")
    print("3. Display publication details")
    print("4. Exit to main menu")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        # Add new publication
        title = input("Enter title: ")
        author = input("Enter author: ")
        year = int(input("Enter year: "))
        isbn = input("Enter ISBN: ")
        book_type = input("Enter book type: ")
        new_publication = Book(title, author, year, isbn, book_type)
        library.add_publication(new_publication)
        handle_publication_management()
    elif choice == 2:
        # Search for a publication
        title = input("Enter title to search: ")
        publications = library.search_publication(title=title)
        if publications:
            print("Publication found in the library.")
        else:
            print("Publication not found in the library.")
        handle_publication_management()
    elif choice == 3:
        # Display publication details
        title = input("Enter title to display details: ")
        publications = library.search_publication(title=title)
        if publications:
            for publication in publications:
                publication.display_details()
        else:
            print("Publication not found.")
        handle_publication_management()
    elif choice == 4:
        # Exit to main menu
        UserInterface.display_menu()
        choice = int(input("Enter your choice: "))
        UserInterface.handle_menu_choice(choice)
    else:
        print("Invalid choice. Please select a valid option.")
        handle_publication_management()
def handle_loan_management():
    print("\nLoan Management")
    print("1. Lend a Publication")
    print("2. Return a Publication")
    print("3. Display Loan Details")
    print("4. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        # Loan a publication
        member_id = input("Enter member ID: ")
        publication_title = input("Enter publication title: ")

        # Find member and publication
        member = library.search_member(member_id)
        publications = library.search_publication(title=publication_title)

        if member and publications:
            # Display available publications
            print("Available publications:")
            for idx, publication in enumerate(publications, start=1):
                print(f"{idx}. {publication.title}")

            # Select publication to loan
            publication_index = int(input("Enter publication number to loan: ")) - 1
            selected_publication = publications[publication_index]

            # Loan the selected publication
            if library.lend_publication(member, selected_publication):
                print("Publication successfully loaned.")
            else:
                print("Failed to loan publication.")
        else:
            print("Member or publication not found.")

        handle_loan_management()
    elif choice == 2:
        # Return a Publication
        member_id = input("Enter Member ID: ")
        publication_title = input("Enter Publication Title: ")

        # Find member and publication
        member = library.search_member(member_id)
        publication = library.search_publication(title=publication_title)
    
        if member and publication:
        # Find loan associated with the member and publication
            found_loan = None
            for loan in library.loans:
                if loan.member == member and loan.publication == publication[0]:
                    found_loan = loan
                    break

            if found_loan:
            # Perform return using the Loan object
                if found_loan.return_publication(publication[0], library):
                    print("Publication returned successfully")
                else:
                    print("Failed to return publication")
            else:
                print("No loan found for this member and publication")
        else:
            print("Member or publication not found")

        handle_loan_management()

    elif choice == 3:
        # Display Loan Details
        member_id = input("Enter Member ID: ")
        publication_title = input("Enter Publication Title: ")

    # Find member and publication
        member = library.search_member(member_id)
        publications = library.search_publication(title=publication_title)
    
        if member and publications:
            found_loan = None
            for loan in library.loans:
                if loan.member == member and loan.publication == publications[0]:
                    found_loan = loan
                    break
        
            if found_loan:
                print("Loan Details:")
                print("Member:", found_loan.member.name)
                print("Publication:", found_loan.publication.title)
                print("Loan Date:", found_loan.loan_date)
                print("Due Date:", found_loan.due_date)
            else:
                print("No loan found for this member and publication")
        else:
            print("Member or publication not found")
        handle_loan_management()


    elif choice == 4:
        UserInterface.display_menu()
        choice = int(input("Enter your choice: "))
        UserInterface.handle_menu_choice(choice)
    else:
        print("Invalid choice. Please select a valid option.")


def handle_reports():
    print("\nReports")
    print("1. Generate overdue loans report")
    print("2. Generate popular publications report")
    print("3. Exit to main menu")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        library.generate_overdue_loans_report()
        handle_reports()
    elif choice == 2:
        library.generate_popular_publications_report()
        handle_reports()
    elif choice == 3:
        UserInterface.display_menu()
        choice = int(input("Enter your choice: "))
        UserInterface.handle_menu_choice(choice)
    else:
        print("Invalid choice. Please select a valid option.")
        handle_reports()

class UserInterface:
    @staticmethod
    def display_menu():
        print("\nMain Menu")
        print("1. Member Management")
        print("2. Publication Management")
        print("3. Loan Management")
        print("4. Reports")
        print("5. Exit")

    @staticmethod
    def handle_menu_choice(choice):
        while True:
            if choice == 1:
                handle_member_management()
                break
            elif choice == 2:
                handle_publication_management()
                break
            elif choice == 3:
                handle_loan_management()
                break
            elif choice == 4:
                handle_reports()
                break
            elif choice == 5:
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please select a valid option.")
                break

if __name__ == "__main__":

    library = Library()
    member1 = Member("Chittapon Booyapataroo", "630911143", "Booyapataroo_c@su.ac.th")
    book1 = Book("How to Good at LOL", "YasuoInwza007", 2020, "978-0-13-458971-7", "Gaming")
    library.add_member(member1)
    library.add_publication(book1)
    UserInterface.display_menu()
    choice = int(input("Enter your choice: "))
    UserInterface.handle_menu_choice(choice)
