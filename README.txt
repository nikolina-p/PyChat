SETUP INSTRUCTIONS:

Place folder on path on your computer in which you can run python code.

1. SETUP THE DATABASE:
    a. run "python db_setup.py"
       - in terminal, navigate to the PyChat/ folder and use command "python db_setup.py"
       to ran the database setup script
    b. run "load_test_data.py"
       - if you want to start with some data already in database, run "python load_test_data.py"
       - if you want clear database, you will have to create users trough user interface (sign up option)
    c. start the http server by ranning "python -m http.server"
    d. start the websocket server by running "python app.py"
    e. open the web browser and type in http://localhost:8000/index.html (do this for each user)


PyChat is a web chat application leveraging Python's 'asyncio' and 'websocket' libraries.
It facilitates concurrent and persistent user connections to the server, processing them asynchronously
for enhanced performance and responsiveness.

FEATURES:
1. User sign up:
    - checks if username already exists; saves new user in the DB and informs all the other active users about new login
2. User log in:
    - checks validity of username and password, informs user about the problem; if ok, reroutes user to the new page and
    informs all the other active users about new login
3. Managing user sessions:
    - on signup/login, every user gets unique session ID that is used latter for user authentication with
    each server call.
    - when user closes the chat window, session ID gets destroyed
4. Exchanging messages:
    - picking the friend from the user list and sendig him/her a message; shows message history; shows "new message"
    notification when message is received from a friend that user is not talking to at the moment; if user is not active
    messages are delivered upon login - sender is informed about late delivery


SPACE FOR IMPROVEMENT
1. Input data sanitization
2. Strong password enforcement
3. Better code organisation in proper modules and better "separation of duties"
