from flask import Flask, session, flash
app = Flask(__name__)

app.secret_key = "shhhhh"

#name of database you are using goes here!
DATABASE = 'shows_db'