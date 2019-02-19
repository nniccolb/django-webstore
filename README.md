# Django webstore project

## Features

    - Authentication

    We implemented the login, logout and register functionalities with email validation.

    - Basic player functionalities

    Buy/play games. Buying happens through the course's provided payment system.
	We also categorized the games so the users can find them more easily.
	Players can only play games which have been bought. Our backend provides the verification.



    - Basic developer functionalities

    A developer can add games by url (and set price etc). Only a developer can add games.
    The statistics of how many times a given game has been bought can be seen in the developer's profile. We did not implement the ability
    to modify or delete games from the webstore. 
    - Game/service interaction

    High scores for games. When a user chooses to submit his/her score the app will add the score to our database of global high scores. The score is received through a Javascript event. The highest 10 scores are shown to players in descending order. 

    - Quality of work

    The code is clean, stuctured and commented. The application is structured as it should be in Django.

    - Non-functional requirements

    Impossible to analyze thoroughly. We made project plan and mostly sticked in it.
    We also made the project as a team - eventhough one of the members has significantly more commits than others. (We often worked as a group and had one computer connected to a large TV display.) 



  
## **IMPORTANT**  
since the email validation works locally in the terminal, you should use pre-existing accounts to log in.

*  For testing the customer's experience use credentials: username: *customer* password: *apple25!*
*  For testing the developer's experience use credentials: username: *developer* password: *banana25!*

  With these accounts you can buy games and play them. Use the developer account to add new games! 


  When pressing register, an activation link will be sent to the user's email, and by pressing the link the user will be redirected to the frontpage of our app.
  
  In the frontpage we have categories for games, and by selecting a category it takes the user to the page where all the games from specific category are listed. 
  To buy a game, the user needs to press the game name in the game view.
  
  **The high score feature only works on our primary game, "Ball game",** as we did not implement the score system on our other game,
  "Sun Jump". Sun Jump was a group project Jonatan was part of 2 years ago and was only added to the web store as a demo. 

  Registered users can also check their profile, where the user can see a list of developed and bought games.

  If user is a developer, a game can be added from nav-button in top-right corner "Add game". It opens a form for the developer to enter the required, specific details about the game. 
