from sqlalchemy import Column, String, create_engine, Integer, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import joinedload

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    email = Column(String(), unique=True)
    username = Column(String(), unique=True)
    password = Column(String())

    scores = relationship('PlayerScore', back_populates='player')
    
class PlayerScore(Base):
    __tablename__ = 'player_scores'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    score = Column(Integer, default=0)

    player = relationship('Player', back_populates='scores')
    player_name = Column(String()) 

def print_player_scores(player_id):
    player_scores = session.query(PlayerScore).filter_by(player_id=player_id).all()
    for player_score in player_scores:
        print(player_score.id, player_score.player_id, player_score.score)

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
        new_player = Player(email=email, username=username, password=password)
        session.add(new_player)
        session.commit()
        print(f"Player {new_player.username} has been created!")

        player_score = PlayerScore(player=new_player, player_name=new_player.username, score=100)
        session.add(player_score)
        session.commit()
        print(f"Initial score for {new_player.username} has been set!")


def login():
    while True:
        username = input("Please enter your username: ")
        password = input("Enter your password: ")

        user_to_login = session.query(Player).filter_by(username=username, password=password).first()
        if user_to_login:
            print("Welcome to the game!")
            return user_to_login
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

def start_story():
    global player
    global player_score

    
    print("Welcome to... ")
    print ("A Haunting in Flatiron!")
    print ("""The year is 2023, you are living in the city of Denver, Colorado after an early retirement from your career as a detective.
    our previous successes in solving high-profile mysteries has left you independantly wealthy and ready to enjoy a peaceful, quiet life.""")
    print ("""One day, an aquintance, Ms. Hazel Rosewood visits you in your luxurious home overlooking the Rocky Mountains.
    Ms. Rosewood is a crime writer for the New York Times, and she is in town to attend a Halloween party hosted by a wealthy socialite, Ms. Seraphina Thorne.
    The guest of honor at the party is the world-famous psychic Ophelia Waterhouse. She has been hired by Ms. Thorne to perform a seance in her home, in hopes of contacting the spirit of her daughter Evangeline.
    Evangeline died tragically last year, having jumped to her death from her bedroom window after her fiancee broke up with her.
    Ms. Rosewood suspects that Ophelia Waterhouse is a fraud, and she would like for you to come help her detect how she convinces her clients that she is for realz.
    You are reluctant to pull time away from your current obsession with playing Tears of the Kingdom.
    However, you have been getting a little weird from spending so much time alone at home, maybe it would be good to get out and put your brain to work?""")
    print ("The choice is yours, do you want to accompany Hazel to the party and debunk an influential fraud, or stay home and play video games?")
    print("1. Attend Ms. Thorne's Halloween party")
    print("2. Stay home and play TotK, maybe take a nice nap.")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("")
        player_score = session.query(PlayerScore).filter_by(player=logged_in_player).first()
        if player_score is None:
            player_score = PlayerScore(player=logged_in_player, score=0)
            session.add(player_score)
            session.commit()
        player_score.score += 1  
        what_to_wear()
                
    elif choice == '2':
        print("NAH. Life is short but detective work is loooong. You decide to spend the next 24 hours chasing down star fragments. It's a good life. THE END.")
        player_score.score -= 1
        session.commit()
        return 'stay_home' 
    else:
        print("Invalid choice. Please try again.")
        return None
    
    if player_score is not None:
        player_score.score += 1  
        session.commit()
        
    else:
        print("No score found for this player.")

    
def what_to_wear():
    while True:
        print("Now what to wear...")
        print("The party is tonight, so you aren't going to have time to go to Spirit Halloween Store and pick through the remnants, so you have two choices:")
        print("1. Batman. It was your Halloween costume a few years ago.")
        print ("2. Ugh, a clown. You barely remember the Halloween party you hosted last year, you were real drunk. You woke up the next morning and found a clown costume on your bathroom floor. I mean, it would at least be something you haven't done before...")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("You are The Night. The Dark Knight. Proceed to the party")
            print ("""
            

                  T\ T\
                  | \| \
                  |  |  :
             _____I__I  |
           .'            '.
         .'                '
         |   ..             '
         |  /__.            |
         :.' -'             |
        /__.                |
       /__, \               |
          |__\        _|    |
          :  '\     .'|     |
          |___|_,,,/  |     |    _..--.
       ,--_-   |     /'      \../ /  /\\
      ,'|_ I---|    7    ,,,_/ / ,  / _\\
    ,-- 7 \|  / ___..,,/   /  ,  ,_/   '-----.
   /   ,   \  |/  ,____,,,__,,__/            '\
  ,   ,     \__,,/                             |
  | '.       _..---.._                         !.
  ! |      .' z_M__s. '.                        |
  .:'      | (-_ _--')  :          L            !
  .'.       '.  Y    _.'             \,         :
   .          '-----'                 !          .
   .           /  \                   .          .


                   """)
            set_the_scene()
            player_score.score += 1 
            return 'batman'
            
        
        elif choice == '2':
            print("When you laugh, the world laughs with you. But you are not laughing. This clown makeup is bad for your skin, and that is not a joke. None the less, proceed to the party.")
            print("""
       ,---.
     ,'_   _`.
   {{ |o| |o| }}
  {{{ '-'O'-' }}}
  {{( (`-.-') )}}
   {{{.`---',}}}
       `---'    
                  """)
            set_the_scene()
            player_score.score -= 1 
            return 'clown'
            
    
        else:
            print("Invalid choice. Please try again.")


def set_the_scene():
    while True: 
        print ("You decide to attend Ms. Thorne's party. Free food and booze! Not to mention, you hate frauds who prey on the vulnerability of the credulous.")
        print ("""The party is at Ms. Thorne's home in Boulder, near the foothills of the Rocky Mountains. Hazel picks you up in her Ford Focus, and as she drives she tells you some of the background on the Thorne family.
        As a young woman in the 70s, Ms. Thorne had been a success in the popular television sitcom Groovy Times.
        The show aired for seven seasons before it was canceled. Ms. Thorne continued to have a moderately successful career as a movie actress, but she put her career on hold to take care of her baby daughter Evangeline.
        Evangeline seemed to follow in her mother's footsteps, acting in several popular Netflix comedies as a child.
        In late 2019, just before the Covid epidemic officially hit the United States, Evangeline met a young woman named Victoria Crowsworthy and fell deeply in love.
        Despite the quarantines, the young couple quickly became enamored of each other, at first spending hours on FaceTime with each other, and then spending every waking moment in the Thorne home together.
        The couple decided to get married, and planned an opulent wedding to be held once the Covid epidemic came under control.
        However, just as vaccines were becoming widely available, Victoria abruptly broke off the engagement with Evangeline and moved to California.
        Soon, Victoria's Instagram filled up with pictures of her and a new love, the wealthy child of a famous Hollywood music producer. Evangeline was devastated.
        Over the next year Evangeline's mental and physical health declined, and then one night in the fall of 2022 she jumped to her death from a high window of her mother's Boulder home.
        Her traumatized mother, Seraphina, has rarely been seen in public since, therefore the information that she would be hosting the famous psychic Ophelia Waterhouse in her home quickly became a subject of speculation and gossip on social media.""")
        print ("You arrive at the home of Ms. Thorne, park the car, and approach the front door. You can hear music and drunk party-goers inside. You knock on the door and a person dressed as Frankenstein opens the door.")
        print ("Do you....")
        print (" 1. Shout TRICK OR TREAT Hahaha just kidding.")
        print (" 2. Hello, I am the renowned detective that Ms. Thorne has hired. Remember how you're dressed.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("The person at the door manages to glare at you strongly enough that you feel the contempt, which is impressive given that they're wearing a latex mask. You ignore it and step inside.")
            halloween_party()
            player_score.score += 1 
            break

        elif choice == '2':
            print("Through the holes in the latex mask, you can see Frankenstein's eyes narrow with skepticism, but they don't question you, they just stand aside as you step into the party.")
            halloween_party()
            player_score.score -= 1 
            break

        else:
            print("Invalid choice. Please try again.")



def halloween_party():
    while True:
        print("""You step into the party. The Thorne home was originally built in 1877. The old building is strewn with Halloween decorations. Hazel helps herself to a glass of wine at the refreshments table.
        As she sips her wine, Hazel explains that there has been a long history of tragedy in this house. A wealthy man built this house for his family, and a few years later everyone in the family died of tuberculosis,' says Hazel. 'Everyone who has lived in this house reports instances of strange phenomenon, the rumor is that the house is haunted by the people who have died here.
        You are skeptical of claims of supernatural phenomenon. It is your opinion that such occurrences are rooted in human psychology, not in otherworldly entities.""")
        print("Do you choose to express your skepticism, or to remain silent?")
        print("1. Speak your mind. They hired you because you figure out problems by observing the REAL world.")
        print("2. Keep your mouth shut; you are just here to get out of the house. There will be plenty of time to debunk nonsense in the sEAnCE.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Oh, I see. Ms. Thorne is clinging to superstition rather than dealing with her trauma. That seems healthy. Not like she can afford a therapist.' you say while smirking.")
            halloween_party_two()
            player_score.score += 1 
            break

        elif choice == '2':
            print("'Uh huh. Interesting.' you mumble while shoving cubes of cheese into your mouth.")
            halloween_party_two()
            player_score.score -= 1 
            break

        else:
            print("Invalid choice. Please try again.")


def halloween_party_two():
    while True:
        print ("""Hazel shrugs and goes to mingle with other guests until it's time to start the seance.
        You glance around the room. There are many guests throughout the main floor of the home.
        You don't know anyone, so you decide to explore the home.""")
        print ("1. There is a room to the left of the entry hall. You can see a glowing fireplace and bookshelves lining the walls. Time to inspect the library! For purely professional reasons, of course.")
        print ("2. There is a sitting room a little further down the hall, you go see if you can find a comfortable chair until the seance begins.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("You choose to go into the library, it looks so warm and inviting. ")
            library()
            player_score.score += 1 
            break

        elif choice == '2':
            print("You decide to find a comfortable chair in the sitting room, maybe chat with other guests.")
            sitting_room()
            player_score.score += 1 
            break
        
        else:
            print("Invalid choice. Please try again.")

def library():
    while True:
        print ("""You step into the library and, to your surprise, there is a young child sitting in an armchair near the fire reading a book
        This seems odd to you, because there are hardly any other children at this party.
        Hello, what are you reading? You ask, and immediately cringe. You hate it when people interrupt your reading. You have no idea how to talk to kids.
        The child, about ten years old, looks up from their book and holds it out for you to read the title. POISONOUS PLANTS OF NORTH AMERICA
        Huh. That's an interesting choice, you comment awkwardly.
        My dad says that plants, even poisonous ones, can be medicine if used properly. I am gong to be a doctor just like he is, when I grow up, says the child.
        You infer that his must be the child of Dr. Nathanial Foxcroft, a celebrity doctor that has been rumored to be dating Ms. Thorne. You note it to yourself, but decide not to disturb this bookish kid further.""")
        print ("1. You decide to seek out more amenable company in the sitting room.")
        print ("2. Or, you can step outside and enjoy fresh air on the patio.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("The sitting room is calling to you. ")
            sitting_room()
            player_score.score += 1 
            break

        elif choice == '2':
            print("Fresh air sounds nice, you'll go out to the patio.")
            patio()
            player_score.score += 1 
            break
        
        else:
            print("Invalid choice. Please try again.")

def sitting_room():
    while True:
        print("""You decide to wander into the sitting room. It's getting later and the guests are starting to thin out, but one person is sitting on a sofa, looking bored.
        You take a seat across from them and introduce yourself.
        The guest introduces herself as Cassandra Troy and explains that she's there as an assistant to Ms. Waterhouse, who is at present meditating privately in a guest room upstairs, in order to prepare her aura for the upcoming event.
        You believe you detect a note of cynicism and drunkenness in Ms. Troy's voice, so you ask how she came to work for Ms. Waterhouse.
        Oh, you know, I answered an ad on Craigslist years ago. It was an ad looking for a discreet, trustworthy assistant. When it turned out she was a so-called psychic looking for an actual assistant, I figured it was a much easier job than I had expected. Pays well too. And it better pay well, moody old bat that she is,' said Cassandra. 'To tell you the truth, I'm just about done with this job. I'm planning to move on to better things soon.'
        You make a mental note of the comments and move on to the patio area. By this time almost all of the other guests are gone or leaving.""")
        print("1. Go back to the library, but you have a feeling you've seen all there is to see there.")
        print ("2. Go out to the patio, the booze fumes in this house are a lot.")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("You've already been to the library, no reason to go back, but...")
            library()
            break

        elif choice == '2':
            print("You're going out to the patio.")
            patio()
            break

        else:
            print("Invalid choice. Please try again.")

def patio():
    while True:
        print("""It's a chilly night, but with the small fire burning in the firepit on the brick patio, it's quite comfortable outside. It's a clear night, and the sky is full of stars. You enjoy gazing at the sky for a few moments until your peace is interrupted by a loud snore.
        You turn around and sprawled in one of the Adirondack chairs is a middle-aged man, passed out and snoring loudly. You debate going inside and letting him sleep, but it's getting late and you don't want to leave this person alone outside on a cold night, especially if the fire goes out. You gently nudge his shoulder, and he wakes up with a start.
        'Oh, shit. I fell asleep again. I have been so tired lately, and I'm not used to staying up this late.'
        The man introduces himself as Dr. Foxcroft.
        Dr. Foxcroft goes on to say, 'If Seraphina hadn't insisted I be here, I would never have stayed out this late. Personally, I don't buy into all this ghost nonsense, but maybe it will help her feel better.'
        Just then, the two of you hear the large antique grandfather clock in the entryway chime the quarter-hour. It's 11:45 pm, and the seance is due to start at midnight. You and Mr. Foxcroft make your way inside and join the small group gathering in the sitting room. """)
        print ("1. Go inside to attend the seance.")
        print ("2. Actually there's no real choice here, go inside to the seance.")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("Uhg, let's get this nonsense over with")
            seance()
            player_score.score += 1 
            break

        elif choice == '2':
            print("You hate to admit it, but you're interested to see what will happen.")
            seance()
            player_score.score += 1 
            break

        else:
            print("Invalid choice. Please try again.")



def seance():
    while True:
        print ("""The small group of seance attendees have gathered in the sitting room. Hazel, your writer friend who invited you to this party. Dr. Foxcroft, looking rumpled and tired. Ms. Troy, assistant to the famous psychic, who is directing everyone to leave their phones on the coffee table as no recording devices will be permitted in the seance room. And of course, you. To your surprise, the weird kid from the library comes into the sitting room as well.
        Dr. Foxcroft greets the child: 'Adelaide! I almost forgot you are here, do you have my medication?' The child nods and takes an orange prescription bottle from their pocket, removes a couple of pills from the bottle, and hands them to their father.
        You find this role-reversal between father and child odd. 'Hello Adelaide, is someone going to wait with you in the sitting room while we attend the seance?' you ask.
        'Oh, I'm not waiting in here. I'm going to the seance too.' says Adelaide. 'I miss Evangeline, she was so nice to me.'""")
        print ("""At that moment Ms. Thorne walks into the room. She has a glamorous presence, although her vibe is anxious and uncomfortable.
        Ms. Thorne leads everyone upstairs to the bedroom that belonged to her daughter, it hasn't been changed since her daughter's death. This is where they seance will be held.
        In the room is a round table with chairs for each guest, and an elderly woman sitting in one of the chairs.""")
        print ("""The scene is set in a dimly lit room adorned with Halloween decorations. A long wooden table is at the center, surrounded by plush chairs. A well-dressed hostess, Mrs. Thornton, and her guests gather around the table. At the head of the table sits the dubious psychic, Madame Zara, her eyes shrouded in mystery.
        Ms. Thorne: Welcome, everyone, to this most auspicious Halloween night. We've assembled here in the hopes of reuniting with my dear departed daughter, Emily. Madame Zara, we place our trust in your extraordinary abilities.
        Madame Waterhouse: Fear not, dear Mrs. Thornton. The spirits shall be with us tonight. Now, if you would all join hands and close your eyes. Let us create a circle of energy to bridge the gap between the living and the departed.
        The guests obey and form a circle, closing their eyes.
        Madame Waterhouse: (whispers incantations under her breath)
        The room grows colder. A soft, eerie wind rustles the curtains. The candles on the table flicker.
        Cassandra Troy: (nervously) Do you feel that? It's like a chill in the air.
        Hazel Rosewood: (whispering) This is incredible!
        Dr. Foxcroft: (whispering) I can sense something... someone here.
        Madame Waterhouse: (raising her voice) Spirits of the beyond, heed my call! Reveal yourselves!
        A faint, ghostly whisper fills the room, barely audible.
        Madame Waterhouse: (feigning surprise) Emily, is that you? Speak to us!
        Madame Zara's body begins to tremble, and her voice takes on an otherworldly tone.
        "Evangeline!" (through Madame Waterhouse): (in a distant, ethereal voice) Mother... ?
        Mes. Thorne: (tearfully) Evangeline, my dear, we tried to protect you!
        "Evangeline" (through Madame Waterhouse): (accusingly) But...I was betrayed me! I was...MURDERED!
        The guests exchange nervous glances, their faces etched with shock and suspicion.
        Ms. Rosewood: (stammering) Th-this is nonsense!
        Ms. Troy: (defensive) No one here could have done such a thing!
        Madame Waterhouse: (returning to her normal voice, with a knowing smile) My dear guests, it seems that the spirits have spoken tonight. But remember, the world of the supernatural is a mysterious one, and not all is as it seems.
        Madame Waterhouse's body relaxes, and the eerie presence in the room dissipates.""")
        print ("....WOW. That was a lot. ")
        print (" You had better head downstairs with the other guests to decompress.")
        print ("1. Go downstairs with the other guests.")
        print ("2. GTFO. This is toooo much.")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("""As you and the others walk down the stairs, Hazel says,"can you believe this drama?? """)
            murder()
            player_score.score += 1 
            break

        elif choice == '2':
            print("Yeah, I'm going down the stairs. And then I'm going right out that door.")
            termination_one()
            player_score.score -= 1 
            break

        else:
            print("Invalid choice. Please try again.")

def murder():
    while True:
        print ("""The guests get up from the table and go downstairs. Gathered in the sitting room, everyone is agitated. Except for little Adelaide, who seems thoughtful. Madame Waterhouse has remained upstairs to gather her thoughts.      
        The guests disperse throughout the house, presumably to gether their possessions and leave, when suddenly there is a blood-curdeling scream from upstairs.
        You and Hazel rush up the stairs together to the bedroom where the seance and find the bedroom window open. You look out the window and there is Madame Waterhuose, dead on the brick courtyard below!""")
        print ("What do you make of this ghastly scene?")
        print ("1. Someone in this house has murdered Madame Waterhouse.")
        print ("2. Clearly ghosts did it. You were skeptical before, but now you've seent it. ")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("You didn't get this far in your detective career by NOT asking questions. A person commited this crime, and your are going to find out who dunnit.")
            who_to_question()
            player_score.score += 1 
            break

        elif choice == '2':
            print("Twas ghosts. Time to go home and maybe take up religion. And drinking.")
            termination_one()
            player_score.score -= 1 
            break
        
        else:
            print("Invalid choice. Please try again.")

def termination_one():
    while True:
        print("""You knew it was a bad idea to leave your comfy home to involve yourself in other people's drama. You don't even wait for Hazel, you call a Lyft and you go directly home. You spend the next six months reading Reddit threads about supernatural activity with intense focus. One mornnig you wake up and wonder if it was all real, or if your need to get away from the stress of detective work let you convince yourself that you had a supernatural experience. That question will remain with you for the rest of your life. At least you have plenty of time for video games. THE END. """)
        break 

def who_to_question():
    while True: 
        print("""You know everyone who was in the house at the time that Madame Waterhouse was murdered. Hazel was with you the whole time, so you know she didn't do it. That leaves her assistant, Ms. Troy; Ms. Thorne; The Doctor; and of course, his creepy kid. Who do you want to question?""")
        print("1. Ms. Troy, the assitant.")
        print("2. Ms. Thorne, the hostess.")
        print ("3. Dr. Foxcroft is an odd one, question him first.")
        print ("4. The creepy kid. Err, I mean Adelaide. ")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Ms. Troy, the assitant, seems to have some resentment toward her boss. Question her.")
            question_Troy() 
            break

        elif choice == '2':
            print("Ms. Thorne seems unstable, question her.")
            question_Thorne()
            break

        elif choice == '3':
            print("")
            question_Foxcroft()
            break

        elif choice == '4':
            print("")
            question_Adelaide()
            break
        
        else:
            print("Invalid choice. Please try again.")

def question_Troy():
    while True:
        print ("Troy, did you do it. Nah, she says.")
        print ("Do you believe her?")
        print ("1. Yes, I believe Ms. Troy")
        print ("2. Nah, Ms. Troy did the thing.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Troy couldn't have done it, back to the drawing board.")
            who_to_question()
            break

        elif choice == '2':
            print("Yeah, it was Troy. Shameful.")
            troy_did_it()
            break
        
        else:
            print("Invalid choice. Please try again.")

def question_Thorne():
    while True:
        print ("Thorne.You do it?? NAH, she says.")
        print ("Plausible?")
        print ("1. Yes, believe Ms. Thorne")
        print ("2. Ms. Thorne is a lying liar, she did the thing.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Thorne couldn't have done it, back to the drawing board.")
            who_to_question()
            break

        elif choice == '2':
            print("Yeah, it was Thorne. Shameful.")
            thorne_did_it()
            break
        
        else:
            print("Invalid choice. Please try again.")

def question_Foxcroft():
    while True:
        print ("Fess up Foxcroft, you do it?? Nope, says he.")
        print ("Truthy or Falsey")
        print ("1. Dr. Foxcroft is innocent.")
        print ("2. Foxcroft did it!!")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Foxcroft couldn't have done it, back to the drawing board.")
            who_to_question()
            break

        elif choice == '2':
            print("Yeah, it was Foxcroft. Shameful.")
            foxcroft_did_it()
            break
        
        else:
            print("Invalid choice. Please try again.")

def question_Adelaide():
    while True:
        print ("Addie, did you do it? No, and it's Adelaide, she says.")
        print ("Come on, do you really think this creepy creepy kid could do it?")
        print ("1. Uh, yeah I do think this creepy kid did it.")
        print ("2. No, of course ADELAIDE didn't do it.")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Adelaide couldn't have done it, back to the drawing board.")
            who_to_question()
            break

        elif choice == '2':
            print("Yeah, it was Adelaide. Shameful.")
            adelaide_did_it()
            break
        
        else:
            print("Invalid choice. Please try again.")

def troy_did_it():
    while True:
        print("Troy did it. How awful. THE END.")
        termination2()
        break 

def thorne_did_it():
    while True:
        print("Thorne did it, can you believe?? THE END")
        termination2()
        break

def foxcroft_did_it():
    while True:
        print("Foxcroft, I knew it, terrible. THE END.")
        termination2()
        break

def adelaide_did_it():
    while True:
        print("Adelaide, you're going to juvie.Sad. THE END. ")
        termination2()
        break


def termination2():
    global logged_in_player

    player_score = (
        session.query(PlayerScore)
        .filter_by(player=logged_in_player)
        .options(joinedload(PlayerScore.player))
        .first()
    )

    if player_score is not None:
        print(f"Your final score: {player_score.score}")

        if player_score.score > 100:
            print("Congratulations! You have a high score. Here's a skull for you:")
            print("   ____")
            print("  / __ \\")
            print(" / /  \\ \\")
            print("| | () | |")
            print(" \\ \\__/ /")
            print("  \\____/")
        elif player_score.score < 100:
            print("You have a score less than 100.")
        else:
            print("Your score is exactly 100.")

    print("Good job, you solved the crime. You are a fabulous detective and also quite stylish, but if you still have that clown costume you should burn it. THE END")
    print_player_scores(logged_in_player.id)


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
            print("6. Start Story")
            
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
        elif choice == '6' and logged_in_player is not None:
            start_story()
            if choice == 'attend_party': 
                what_to_wear()
        else:
            print("Invalid option. Please try again.")
