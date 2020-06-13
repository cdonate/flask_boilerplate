# Boilerplate API

The goal of this project is to be used as a Boilerplate API for microservices.

## Packages

### PyPi

In python, it's important to isolate all your packages by project. So you can use the Pycharm to create a new Virtual Env or you can use directly by your terminal.
If you want to install via PyCharm, follow the link:
https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

If you want to install in your terminal, follow the link:
https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b

Now if you install a package it will be only installed in your custom env.

You can use pycharm to install your packages, or you can use the terminal to do it so. 
Example of usages:

	$ pip install mypackage
You can pass a file too:

	$ pip install -r myfile.txt

In python we use the file requirements.txt to store our packages. Check the file in the root of the project.

### To Develop

#### System Libs

You need to have some libs pre-installed in your system.
Start with:
	
	$ sudo apt-get update

Then you should install:

	$ sudo apt-get install postgresql python-psycopg2 libpq-dev python3-dev

##### Pitfall

You may find an error while installing the psycopg2. To solve it try to fix the version of python-dev in your install.

    $ sudo apt-get install pythonX.Y-dev
    
Example:

    $ sudo apt-get install python3.5-dev

#### Install

First of all you need to create a custom VirtualEnv.
After you should use:

    $ pip install -r requirements.txt
 
And for tests:

    $ pip install -r requirements_dev.txt


## DOCKER
Docker is a set of platform-as-a-service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.
Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels.
All containers are run by a single operating-system kernel and are thus more lightweight than virtual machines.

The service has both free and premium tiers. 
The software that hosts the containers is called Docker Engine.
It was first started in 2013 and is developed by Docker, Inc.

### Build

To build your project the docker will use the Dockerfile. 
So you need to add some lib or anything in specific, you should update the Dockerfile.
To build you project, run:

    $ docker build --build-arg PORT=${PORT} --build-arg=GUNICORN_WORKERS=${GUNICORN_WORKERS} -t flask_boilerplate_api .
    
### RUN

When the docker image is ready, you can run it using:

    $ docker run -p ${PORT}:${PORT} --env-file .env --name flask_boilerplate_api flask_boilerplate_api
    
## Database

By default, we usually use Postgresql to deal with the database.
All tables are stored in the file models.py. 
If you need to use a table, you should not allow that a database model object is leaked to other layers of your project.
So if you have a table like PersonTable, you should be a class called Person that uses and encapsulate the database actions.

### Creating the database:

This is an example of how you could create your database:

    $ sudo su postgres
    $ psql
    $ CREATE ROLE boilerplate_api SUPERUSER LOGIN PASSWORD 'boilerplate_api';
    $ CREATE DATABASE boilerplate_api;
    $ ALTER DATABASE boilerplate_api OWNER TO boilerplate_api;
    $ \q

### Migrates

Migrations are Python’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. 
They’re designed to be mostly automatic, but you’ll need to know when to make migrations, when to run them, and the common problems you might run into.

In this project, we use Alembic to manage our migrations.
We have a command that creates the migrations and other that applies the migrations.

#### Create Migrations
To create the migrations, be sure that you have the environment loaded and run:

	$ python manage.py db migrate

#### Apply Migrations
It's always good to verify if the migrations were created correctly.
To apply these migrations just run:

	$ python manage.py db upgrade