# Bucketlist API(Checkpoint 2)

[![Build Status](https://travis-ci.org/andela-amutava/Bucketlist.svg?branch=master)](https://travis-ci.org/andela-amutava/Bucketlist)
|
[![Coverage Status](https://coveralls.io/repos/github/andela-amutava/Bucketlist/badge.svg?branch=master)](https://coveralls.io/github/andela-amutava/Bucketlist?branch=master)

BucketList API is a simple application built using the flask microframework. It's an application that helps users track what they want to do in the future.


| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register` | `POST`  | Register a new user|
|  `/auth/login` | `POST` | Login and retrieve token|
| `/api/bucketlists` | `POST` | Create a new Bucketlist |
| `/api/bucketlists` | `GET` | Retrieve all bucketlists for user |
| `/api/bucketlists/?limit=2&page=1` | `GET` | Retrieve one bucketlist per page |
| `/api/bucketlists/<id>` | `GET` |  Retrieve bucket list details |
| `/api/bucketlists/<id>` | `PUT` | Update bucket list details |
| `/api/bucketlists/<id>` | `DELETE` | Delete a bucket list |
| `/api/bucketlists/<id>/items` | `POST` |  Create items in a bucket list |
| `/api/bucketlists/<id>/items/<item_id>` | `DELETE`| Delete a item in a bucket list|
| `/api/bucketlists/<id>/items/<item_id>` | `PUT`| update a bucket list item details|

### Installation
1. Create a folder.
` `
2. Clone the repository into the given folder.
`https://github.com/andela-amutava/Bucketlist.git`
3. Navigate to the project folder. 

4. Install project dependencies in your virtual environment.
` pip install -r requirements.txt`

5. Install the project dependencies from the requirements.txt file.
6.Set up project development. Run db migrations.
`
 python manage.py db init
 python manage.py db migrate
 python manage.py db upgrade
`
7. Run the server.
`python manage.py runserver`

##Testing
`You can run the tests nosetests --with-coverage`