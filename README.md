# Oblivion

* Bi-directional Chat application
* User Registration and login
* Multiple rooms
* Unique urls for each room
* share and save room


## Packages Used

* Python Flask
* Javascript
* SocketIO & Flask-SocketIO
* WTForms
* SQLAlchemy
* Postgresql Database
* Rethinkdb Database


## Getting Started

### Install Packages
```
pip install virtualenv
virtualenv venv
source venv/bin/activate (for windows venv\Scripts\activate)
pip install -r requirements.txt
```
[install server](https://www.rethinkdb.com/docs/quickstart/)


### Create Databases

[Start rethinkdb server](https://www.rethinkdb.com/docs/quickstart/)
```
python main.py rethinkDbSetup  (create Thinkdb database and tables)
python main.py shell
db.create_all()                (to create Postgresql database and tables)
```

### Running Application

Start rethinkdb server

```
python main.py run

```

# Stil Todo

* user __Bleach__ to sanitize  user input to make it more secure. 

# Demo

### Register User and Login
![link for gif]( https://github.com/ObsidianRock/Oblivion-Chat/blob/master/video/register_1.gif "Register and Login")


## Adding new room and saving room
![link for gif](https://github.com/ObsidianRock/Oblivion-Chat/blob/master/video/add%20and%20save%20room.gif "New and Save room")


## Chat application
![link for gif](https://github.com/ObsidianRock/Oblivion-Chat/blob/master/video/chat_22.gif "Chat Application")
