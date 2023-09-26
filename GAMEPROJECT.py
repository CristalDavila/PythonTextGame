from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    email = Column(String(), primary_key=True)
    username = Column(String(), unique=True)
    password = Column(String())

engine = create_engine('sqlite:///players.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_player():
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")

    existing_player = session.query(Player).filter_by(username=username).first()
    if existing_player:
        print("Player already exists.")
    else:
        new_player = Player(username=username, password=password, email=email)
        session.add(new_player)
        session.commit()
        print(f"Player {new_player.username} has been created!")

def login():
    while True:
        username = input("Please enter your username: ")
        password = input("Enter your password: ")

        user_to_login = session.query(Player).filter_by(username=username, password=password).first()
        if user_to_login:
            print("Welcome to the game!")
        else:
            print("Invalid username or password. Please check your credentials.")

def delete_player():
    username_to_delete = input("Enter the username of the player to delete: ")
    player_to_delete = session.query(Player).filter_by(username=username_to_delete).first()
    
    if player_to_delete:
        session.delete(player_to_delete)
        session.commit()
        print(f"Player {username_to_delete} has been deleted.")
    else:
        print("Player not found.")

def update_email(player):
    new_email = input("Enter your new email: ")
    player.email = new_email
    session.commit()
    print(f"Email for {player.username} has been updated to {new_email}.")

if __name__ == '__main__':
    logged_in_player = None  

    while True:
        if logged_in_player is None:
            print("Please log in or create a new player.")
            print("\n1. Log in")
            print("2. Create a new player")
            print("3. Delete a player")
        else:
            print("4. Update Email")
            print("5. Logout")

        choice = input("Select an option: ")

        if choice == '1' and logged_in_player is None:
            logged_in_player = login()
        elif choice == '2' and logged_in_player is None:
            create_player()
        elif choice == '3' and logged_in_player is None:
            delete_player()
        elif choice == '4' and logged_in_player is not None:
            update_email(logged_in_player)
        elif choice == '5' and logged_in_player is not None:
            logged_in_player = None
        elif choice == '5' and logged_in_player is None:
            break
        else:
            print("Invalid option. Please try again.")
