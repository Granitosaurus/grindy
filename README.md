# Grindy
Grindy is a command line application for long term memory(LTM) training. Application uses user created decks with question & answers to question the user using question rating algorithms and other LTM methods.

# Installation
    pip3 install GIT+https://github.com/Granitas/grindy
Run grindy:  

    grindy -init
to initiate the program to `home/grindy` directory or add optional argument `--location` for a different location

# Starting  

First thing you need question decks, grindy comes with few default decks you can see via command:

    grindy -l
    > Decks found:                                                                           
    > --------------------------------------------------------------------------------       
    > - alphabet                                                                             
    > - months    
   
To open a deck use `grindy -o deck_name`:

    grindy -o alphabet
    > Opening deck "alphabet":                                                               
    > ________________________________________________________________________________
    > Q: 11  
    > A: 

# Answering

By default there are 4 answer states:  
*  correct - 100% match  
*  partial_high - over 80% match  
*  partial_low - over 60% match   
*  incorrect - anything under that  

they all increase the question rating, when question reaches 100% it is considered to be in LTM however the ratings decrease over time (even though quite slowly)

**To finish the session use CTRL+D** which will save deck and return some session statistics

#### Arguments

It is possible to use various arguments when answering the questions
Currently available arguments:  
* `-quit`: quits the program  
* `-h`: prints a hint  
* `-r`: prints current rating  
* `-set_hint <value>`: changes the hint of the question  
* `-t`: prints how many times the question was answered  
* `-lr`: prints when was the Last Run of the question  
* `-set_rating <value>`: sets rating to provided value  

e.g.:  

    Q: creator of Python?                                                           
    A: -h
    Hint: G**d* *** *o*s**  # If no hint exists grindy generates one (can be disabled with -nah argument)                                                      
    A: -set_hint how can you not know?
    Setting question hint to "how can you not know?"                                
    A: -h
    Hint: how can you not know?                                                     
    A: 

# Creating and Downloading decks

Decks are simple .json files that follow this structure:
    {"questions": [<list fo questions>]
    where question is made up of these values: answer, rating, question, streak, times, last_run, hint
    
To create a deck you can use `grindy -md` which will start input sequence. i.e.

    grindy -md github  
    > Q: when did github launch?      
    > A: 2008-04-10 -h The same year Beijing Olypic games started  
    > CTRL+D  
    > Q: deck github has been saved!  
    grindy -o github  
    > Opening deck "github":                                                            
    > ________________________________________________________________________________  
    > Q: when did github launch?                                                       
    > A: -h  
    > Hint: The same year Beijing Olypic games started     

It is also possible to download decks from github repos via `grindy -rl` and `grindy -rdl` or directly from any other source via `grindy -dl`

# Grindy arguments

    optional arguments:
      -h, --help            show this help message and exit
      -o DECK, --open DECK  open deck <deckname>[.json]
      -l, --list            list decks
      -dl [NAME URL [NAME URL ...]], --download [NAME URL [NAME URL ...]]
                            download deck from direct url
      -rl, --repo_list      list decks in the deck repos
      -rdl DECK, --repo_download DECK
                            Download a deck from repo
      -md NAME, --make_deck NAME
                            make a deck
      -del DECK             delete deck
      --reset_deck DECK     reset deck of any progress
      -init                 setup grindy in provided location (no location uses
                            current working directory)
      -loc, --deck_location
                            decks location
      -cs, --case_sensitive
                            set case sentivity on for q&a
      -nah, --no_auto_hints
                            disable auto hints

    