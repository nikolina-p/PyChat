PYChat is my final project for the class "Mastering Python" on UC Berkeley Extension.

It is a web chat application leveraging Python's 'asyncio' and 'websocket' libraries. It facilitates concurrent and
persistent user connections to the server, processing them asynchronously.

Application architecture is designed according to MVC pattern. Adapter pattern is used to add functionality to
classes in the model layer, mainly for calling repository classes.

JavaScript and CSS code was written using ChatGPT significantly. All the Python code is mine.

SETUP INSTRUCTIONS:

    a. copy the PyChat folder to a directory on your computer where you can execute Python code
    b. setup a database - run "python db_setup.py"
       - in terminal, navigate to the PyChat/Database folder and use command "python db_setup.py" to ran the database
       setup script
    c. load test data if you wish - run "load_test_data.py"
       - if you want to start with some data in database, while in Pychat/Database, run "python load_test_data.py"
       - if you want an empty database, you will have to create users through user interface (sign up option)
    d. navigate to PyChat folder, start the http server by running "python -m http.server"
    e. while in PyChat folder, start the websocket server by running "python main.py"
    f. open the web browser and type in http://localhost:8000/index.html (do this for each user)


WHAT WAS DONE:
1. User sign up:
    - checks if username already exists; saves new user in the DB and informs all the other active users about
    new login
2. User log in:
    - checks validity of username and password, informs user about the problem; if ok, reroutes user to the
    new page and informs all the other active users about new login
3. Managing user sessions:
    - on signup/login, every user gets unique session ID that is used later for user authentication with
    each server call.
    - when user closes the chat window, session ID gets destroyed
4. Exchanging messages:
    - picking the friend from the user list and sending him/her a message; shows message history; shows "new message"
    notification when message is received from a friend that user is not talking to at the moment; if user is
    not active messages are delivered upon login - sender is informed about late delivery


SPACE FOR IMPROVEMENT
1. Input data sanitization
2. Strong password enforcement
