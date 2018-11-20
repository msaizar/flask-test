
# flask-test

For this test project, I've decided to try Flask as the web application and Docker for deployment. 

This cookiecutter Flask template was used: https://github.com/sloria/cookiecutter-flask

I had no prior experience with Flask so this template was of great help. I wanted to have an idea about best practices and a sample project up and running. I used https://github.com/pydanny/cookiecutter-django for other projects before, so I grabbed a lot of things from there for Docker deployment.

I ended up using a MethodView (http://flask.pocoo.org/docs/1.0/views/#method-views-for-apis) for the API and WTForms for the form.

The following tutorial helped a lot for getting up to speed with the backend: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
The frontend is heavily based on another of his tutorials, a rather old one: https://blog.miguelgrinberg.com/post/writing-a-javascript-rest-client

A lot could be improved, main points I'd work on next:

- Frontend testing
- Decouple Frontend/Backend, serve static files and API endpoints only. Use Webpack. Right now the homepage renders a form via Flask, this shouldn't be needed.
- After inserting/updating a feature, the API endpoint returns a list of all features for convenience. It should only return the modified features.
 

## Local Development

On a terminal, bring up the docker containers.
`$ docker-compose -f local.yml up --build`

Migrate the database on another terminal.
`$ docker-compose -f local.yml run --rm flask-test flask db upgrade`

Navigate to http://localhost:5000


Run backend tests.
`$ docker-compose -f local.yml run --rm flask-test flask test`


## Production

Copy `.envs/local/.env` to `.envs/production/.env`

You'll need to make some modifications to the copied file:

Change the `FLASK_ENV` variable to `production`.
`FLASK_ENV=production`

Change the secret key.
`SECRET_KEY="not-so-secret"`

Change the Postgres credentials.
`POSTGRES_USER=flasktest`
`POSTGRES_PASSWORD=flasktest`
`POSTGRES_DB_NAME=flasktest`


Create an EC2 instance with Docker Machine. You'll need your AWS credentials configured, see https://docs.docker.com/machine/examples/aws/
`$ docker-machine create --driver amazonec2 flasktest`

Set your environment variables to use docker-compose with this Docker Machine.
`$ eval $(docker-machine env flasktest)`

Bring up the services.
`$ docker-compose -f production.yml up --build -d`

Get the Docker Machine's IP address and navigate to it.
`$ docker-machine ip flasktest`