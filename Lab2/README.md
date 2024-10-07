# Lab 2: Clients and Servers

This is the code for the Lab 2 website.

## Running the Code
This website is written in Python using the Flask framework. To run it:

1. Install Python from https://www.python.org/.
2. Install Flask using the command `python -m pip install flask`.
3. Run the server with the command `python app.py`.
4. View the website by visiting http://localhost:8000.

The server is configured to run in debug mode, meaning it will automatically reload any time the code is modified. If you disable this, you will have to manually restart the server every time you make a change.

## Modifying the Code
This folder contains the following code files:

- app.py: The web server code. This is the only file you need to modify for this lab.
- templates/: The HTML templates served by app.py. You do not need to modify these, but they may help your understanding of how the website operates. These are written using Flask's template system, which allows Flask to insert variables and add additional logic to change how the page is rendered: for more information, see the documentation here: https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/.
- database/: Code used to store and retrieve data. You do not need to modify this code.
- static/: Static assets, like images and CSS files. These are purely aesthetic, and do not matter for the lab.

All of the important code is in `app.py`. This file contains functions which are prefaced with the `@app.route` decorator, such as `@app.route("/some/path", methods=["GET"])`: these functions will run when a user requests the corrosponding path using the given method, and their return value will be sent back to the user. The file also contains several helper functions, which will be useful when making your modifications:
  - get_current_user(): Returns the username of the current user, or None if the user is not logged in.
  - is_admin(user: User): Returns `True` if the given user is an admin, and `False` otherwise.
  - get_user_balance(username: str): Returns the balance of the given user.
  - get_item_price(item_id: int): Returns the price of the given item.
  
The functions in `app.py` also store or retreive information from a database using functions which are defined in the file `database/database.py`, such as `database.update_user_balance`. You do not need to modify any of these functions, and their name should provide enough information about their behavior for you to understand what they do. You are welcome to call them directly if you like, but you should only need the helper functions defined above to complete the assignment.