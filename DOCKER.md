# How to use

## Create Database

Set up a free MongoDB database on [MongoDB Atlas](https://cloud.mongodb.com) or host one locally using Docker.

## Configuration via environment variables

- `MONGODB_HOST` the mongodb host
- `MONGODB_USER` the mongodb user
- `MONGODB_PASS` the mongodb password
- `MONGODB_CLUSTER` use when using the mongodb database of cloud.mongodb.com
- `MONGODB_DATABASE` name your db collection (e.g. `webservice`)
- `MONGODB_COLLECTION` name your db collection (e.g. `shortner`)
- `PORT` your access port
- `HOST` the host

Then run `docker-compose up -d`, now you can access the shortner at <http://localhost:5000/> from your host system.
