# Flask file upload

The goal for this project was to understand how to have multiple
Docker containers or OpenShift pods working together.

## About

This project will create the following environment:

* Container 1: A flask application which accepts file uplaods, adds an
entry within a MySQL database and save the file within a mounted volume
point.

* Container 2: A MySQL database to store entries.

* Container 3: A mounted volume storage on a host system or a OpenShift
pod which is a persistent volume for storage. Which is connected to the
application container.

## System setup

You should first create a new Python virtual environment to install the
required packages.

```bash
$ virtualenv ~/venv
$ source ~/venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Run via Docker

To run the project using Docker containers, you first will need to
build the container images. This is done using docker-compose. Run
the following command to build the images:

```bash
(venv) $ make build-images
```

Once the images are built successfully, you can now start them. Run
the following command to start new containers:

```bash
(venv) $ make start-containers
```

You can now test the application by uploading a file. There is an
example file within the root of this project **example.yml** which you
can use.

```bash
$ curl -F 'file=@example.yml' http://0.0.0.0:5000/upload_yml
```

When the flask application container is booted, a mounted volume is
created at the /tmp directory. If you view the latest files in that
directory, you will see new files being created. These files are the
ones that were uploaded.

You can also login to the container for the database to see the entries
being added.

```bash
$ docker exec -it <container_name> /bin/bash
$ mysql -u root -p
mysql> use kingbob;
mysql> select * from file_entry;
```

## Run via OpenShift

Content comming soon!
