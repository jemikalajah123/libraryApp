# libraryApp
This is a simple library applicaton with basic features, built with django framework.
There are two levels of users, the admin (librarian) and a normal user (student).
Users are able to request to borrow books from the library and admin has to approve before the request is completed.
## APIs Documentation
There is an API documentation built with postman to assist you on understanding the APIs usage. Click here to view the documentation https://documenter.getpostman.com/view/10333949/TzCS45it

## Clone the repository
Run `git clone https://github.com/jemikalajah123/libraryApp.git` to clone the repository to your local.

## Start Development server with docker
Make sure docker is insatlled on your local and is running.
Start the development server on docker with the following commands;

Run `cd libraryApp` to navigate into the root directory.

Run `docker-compose build` from the root directory.

Run `docker-compose up` from the root directory.
## view the App
Navigate to http://0.0.0.0:8000/. The app will not automatically reload if you change any of the source files.

