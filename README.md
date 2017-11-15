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

## Run via Docker

You should first create a new Python virtual environment to install the
required packages.

```bash
$ virtualenv ~/venv
$ source ~/venv/bin/activate
(venv) $ pip install -r requirements.txt
```

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

You will need to stand up a local instance of OpenShift and download
the oc client binary to communicate with OpenShift. You can use any of
the available ways to stand up OpenShift Origin (oc cluster, minishift).

Once you have your OpenShift instance running, run the following
commands to create the pods:

```bash
# create mysql pod
oc new-app --template=mysql-persistent \
--param=DATABASE_SERVICE_NAME=db \
MYSQL_ROOT_PASSWORD=password MYSQL_DATABASE=kingbob \
-l db=mysql

# create flask-file-upload pod
oc new-app rywillia/flask-file-upload MYSQL_DATABASE=kingbob \
MYSQL_ROOT_PASSWORD=password -l app=flask

# expose route for flask application to be accessed externally
oc expose service flask-file-upload --name=flask-file-upload \
-l app=flask

# create persistent volume and attach to flask pod deployoment config
oc set volume deploymentconfigs/flask-file-upload \
--add --mount-path=/mnt/app --name=app-storage --claim-size=1G
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
$ oc exec -it <pod_name> /bin/bash
$ mysql -u root -h <internal_ip_of_pod> -P <pod_port> -p
mysql> use kingbob;
mysql> select * from file_entry;
```

You can run the following commands to clean up your OpenShift pods:

```bash
# delete all objects associated with database pod
oc delete dc,pod,pvc,services,secret -l db=mysql

# delete all objects associated with flask pod
oc delete imagestream,dc,pod,pvc,services,secret,route -l app=flask
```