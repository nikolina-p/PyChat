# PYChat

PYChat is my final project for the **Mastering Python** course at **UC Berkeley Extension**.

It is a web chat application built using Python’s `asyncio` and WebSocket libraries. It supports persistent connections from multiple users and processes their requests asynchronously.

## Architecture

The application follows the **Model–View–Controller (MVC)** architectural pattern. The **Adapter pattern** extends the functionality of classes in the model layer, primarily by providing access to repository classes.

## Authorship

I wrote all the Python code. ChatGPT provided substantial assistance with the JavaScript and CSS code.

## Setup Instructions

1. Copy the `PyChat` folder to a directory on your computer where you can execute Python code.

2. Set up the database. Open a terminal, navigate to `PyChat/Database`, and run:

   ```bash
   python db_setup.py
   ```

3. Optionally, load test data. From the same directory, run:

   ```bash
   python load_test_data.py
   ```

   If you skip this step, create users through the application's **Sign Up** option.

4. Navigate to the `PyChat` folder and start the HTTP server:

   ```bash
   python -m http.server
   ```

5. Open a separate terminal, navigate to the `PyChat` folder, and start the WebSocket server:

   ```bash
   python main.py
   ```

6. Open the following URL in your browser:

   http://localhost:8000/index.html

   Open a separate chat window for each user.

## Features

### User Registration

- Checks whether the username already exists.
- Saves new users to the database.
- Notifies other active users when a new user joins.

### User Login

- Validates the username and password and displays an error if authentication fails.
- Redirects successfully authenticated users to the chat page.
- Notifies other active users when a user logs in.

### Session Management

- Assigns a unique session ID when a user signs up or logs in.
- Uses the session ID to authenticate subsequent requests to the server.
- Invalidates the session ID when the user closes the chat window.

### Messaging

- Allows users to select another user from the user list and send messages.
- Displays message history.
- Shows a new-message notification when a message arrives from someone other than the currently selected conversation partner.
- Delivers messages sent to offline users when they next log in.
- Notifies the sender when a previously undelivered message is delivered.

## Areas for Improvement

- Input validation and sanitization.
- Strong password requirements.

