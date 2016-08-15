# Edit-in-place, Everywhere!

_Everywhere_ is a generic and ultra easy to use edit-in-place concept.
_Everywhere API_ is the data storage and API provider for the editor.


## Technical specifications

Based on [Flask](http://flask.pocoo.org/) and [Flask RestPlus](https://github.com/noirbizarre/flask-restplus), it runs in Python3.

[TinyDB](https://github.com/msiemens/tinydb) is used for storage;
no need to setup a database!


## Installing and running

### Download these sources

    git clone https://github.com/vinyll/everywhere-api.git
    cd everywhere-api

### Run the project with venv

    python3 -m venv venv
    echo '/venv/' >> .git/info/exclude
    source venv/bin/activate
    pip install -r requirements.txt
    python app.py

You could alternatively run the project with Docker (see below).


#### Running in production (Docker)

    docker build --tag everywhere-api .
    docker run --name everywhere-api -p 80:80 -v `pwd`:/app -d

This will create a docker with all requirements. Database will be stored outside
of the docker, in the _data_ folder of the source.


## Available methods

All API methods are exposed on http://localhost:5000/.

You can of course use [HTTPie](https://github.com/jkbrzt/httpie),
[Postman](https://www.getpostman.com/),
[curl](https://curl.haxx.se/) or your favorite HTTP tool.

### Create a new user

Go to http://localhost:5000/#!/users/create_new_user and create a user called "_mywebsite_".

It will return an authentication key phrase. Keep it aside!

### Create a new content

Go to http://localhost:5000/#!/contents/create_or_update_content and create
a new content called "_home_article_" for user "_mywebsite_".

### Read a content

Go to http://localhost:5000/#!/contents/get_content and request the
content called "_home_article_" for user "_mywebsite_".


## Usage

A common usage would be to couple with [Everywhere.js client](https://github.com/vinyll/everywhere.js).

You can also consider serving contents from your website server side (with
Python, NodeJS, PHP or whatever server side language) reading the API.


## License: MIT

View the [LICENSE.txt](https://github.com/vinyll/everywhere-api/blob/master/LICENSE.txt) file
for further details.
