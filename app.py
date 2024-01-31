import os 
# above line imports the python os module which provides a way to interact with the operating system including reading environment variables

from flask import Flask, render_template, request, redirect, url_for
# This line imports specific components from the Flask web framework. The components include:
# Flask: The main class for creating a web application.
# render_template: Used for rendering HTML templates.
# request: Used for handling HTTP requests.
# redirect and url_for: Used for managing URL routing.

from flask_mysqldb import MySQL
#This line imports the MySQL extension for Flask. The extension simplifies the integration of MySQL databases with Flask applications.

app = Flask(__name__)
#This line creates a Flask web application instance with the name of the module or package. This instance (app) is the main entry point for the application.

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')
# These lines configure the MySQL connection parameters for the Flask application. The values are read from environment variables, with default values provided if the environment variables are not set. The configuration includes:
# 'MYSQL_HOST': MySQL host.
# 'MYSQL_USER': MySQL user.
# 'MYSQL_PASSWORD': MySQL password.
# 'MYSQL_DB': MySQL database name.

#Initialize MySQL
mysql = MySQL(app)
#This line initializes the Flask application with the MySQL extension, creating a MySQL connection for the application to use.

@app.route('/') #This line is a decorator that defines a route for the root URL ("/"). The associated function (hello()) will be executed when a user accesses this URL.
def hello(): #This line defines the hello() function. This function will be executed when the root URL is accessed. It connects to the MySQL database, retrieves messages from the 'messages' table, and renders the 'index.html' template with the retrieved messages.
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close() #These lines interact with the MySQL database. It creates a cursor, executes a SELECT query to fetch messages from the 'messages' table, retrieves the results, and then closes the cursor.
    return render_template('index.html', messages=messages) #This line returns the rendered HTML template ('index.html') to the client, passing the retrieved messages to be displayed in the template.

@app.route('/submit', methods=['POST']) #This line is a decorator that defines a route for the "/submit" URL, specifically for HTTP POST requests. The associated function (submit()) will handle form submissions.
def submit(): #This line defines the submit() function, which will be executed when a form is submitted to the "/submit" URL.
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close() #These lines handle the submission of a new message. It retrieves the new message from the submitted form, creates a cursor, executes an INSERT query to add the new message to the 'messages' table, commits the changes to the database, and then closes the cursor.
    return redirect(url_for('hello')) #This line redirects the user back to the root URL ('hello' function) after submitting a new message.

if __name__ == '__main__': #This line checks if the script is being run directly (not imported as a module).
    app.run(host='0.0.0.0', port=5000, debuf=True) # This line runs the Flask application on the specified host ('0.0.0.0'), port (5000), and in debug mode. The host '0.0.0.0' means the application will be accessible from external devices. The debug mode provides additional information for development purposes.
