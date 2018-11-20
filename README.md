# flask-test

Local Development

On a terminal, bring up the docker containers: 

$ docker-compose -f local.yml up --build

Migrate the database on another terminal:

$ docker-compose -f local.yml run --rm flask-test flask db upgrade

Navigate to http://localhost:5000

To run tests:

$ docker-compose -f local.yml run --rm flask-test flask test


Production

You'll need a .env file and configure the following variables:


#FLASK
FLASK_ENV=production
SECRET_KEY="not-so-secret"
FLASK_APP=flask-test/autoapp.py

#POSTGRES
POSTGRES_USER=flasktest
POSTGRES_PASSWORD=flasktest
POSTGRES_HOST=postgres
POSTGRES_DB_NAME=flasktest


First we'll create an EC2 instance with Docker Machine. You'll need your AWS credentials configured.

$ docker-machine create --driver amazonec2 flasktest

Set the environment variables to properly use docker-compose

$ eval $(docker-machine env flasktest)

Now we'll bring it up:

$ docker-compose -f production.yml up --build -d


