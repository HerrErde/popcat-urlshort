<h1 align="center">
  Pop Cat Url Shortner
</h1>

<p align="center">A clone of the Popcat Url Shortner!<p>
<p align="center">
  <a href="https://github.com/HerrErde/popcat-urlshort/commits">
  <img src="https://img.shields.io/github/last-commit/HerrErde/popcat-urlshort"></a>
</p>

<p align="center">
  <a href="https://ko-fi.com/herrerde">
  <img src="https://ko-fi.com/img/githubbutton_sm.svg"></a>
</p>

[![Docker Image](https://github.com/HerrErde/popcat-urlshort/actions/workflows/build-release.yml/badge.svg?branch=master&cacheSeconds=10)](https://github.com/HerrErde/popcat-urlshort/actions/workflows/build-release.yml)

# Setup Instructions

## Create Database

Set up a free MongoDB database on [MongoDB Atlas](https://cloud.mongodb.com)
or host one locally using Docker.

[docker-compose-yml](docker/docker-compose.yml)

### Run local

```sh
cd src
pip install -r requirements.txt
python main.py
```

---

To see how to configure the Docker image, please see [DOCKER.md](DOCKER.md).
