
# Rails on Docker (ROD, a part of XOD)
ROD is like a rocket that brings you from ground (scratch) to the space (Kubernetes).

## Quick Tutorial

> Before start, please check out if you have Docker (version 20.10.12 or later), minikube, and Python (3.6.8 or later) installed on your computer.
### Clone this project and go the directory
```bash
git clone git@github.com:wxw-matt/rails_on_docker.git ~/rod
cd ~/rod
# Install dependencies for rod
pip install -r requirements.txt
```
### Create a Rails project
```bash
./rod project new -v 7 -s first_rod
```
### Add some pages to serve users
```bash
cd first_rod
./rod g scaffold post title:string content:text
```
### Deploy to Kubernetes
```bash
./rod deploy k8s
```
### Expose to users
```bash
./rod deploy service
```
After the previous command performs successfully, you would see the following output:
```bash
service/first-rod created
Service is listening at address http://localhost:port
```
The port varies with each deployment.
### Access the pages
```bash
http://localhost:port/posts
```
## Installation

### System Requirement
Any operating systems that can run Docker (version 20.10.12 or later).

### Commands to Get Rod Ready on Your Computer
```bash
git clone git@github.com:wxw-matt/rails_on_docker.git ~/rod
cd ~/rod
# Install dependencies for rod
pip install -r requirements.txt
```

## Usage

### Create a New Rails Project
The following command will Create a new project named `t1` based on `Rails 7` and using `MySQL` as the database.
```
./rod project new t1 -v 7 -m
```
`project new` is for creating projects.

`-v` or `--version` is for specifying the version of Rails.
Either a complete version, like `7.0.1`, or a major version `7` works.
If a major version is given, the latest major version will be used to create the project.

`-m` or `--mysql` is to select MySQL.

`-p` or `--pg` is to select Postgresql.

`-s` or `--sqlite3` is to select sqlite3.

The docker image for the new image will be created as well.

### Using Rails Generator
Generate a scaffold:

```
./rod g scaffold post title:string content:text
```
Or

```
./rod generate scaffold post title:string content:text
```

Generate a controller
```
./rod g controller article index new create
```

Generate a model
```
./rod g model comment title:string content:text
```

## Executing Rake Tasks
All tasks that can be executed by `rails` command are supported.
For example: you can execute the tasks `db:migrate` and `db:seed` by the following command:
```
./rod tasks db:migrate db:seed
```

# Build images for ARM64 (Apple M1) and AMD64
```bash
tools/build_multiplatform.sh full_tag Dockerfile
```
For example:
```bash
tools/build_multiplatform.sh wxwmatt/rails:7.0.2.2-alpine3.15 rails7/Dockerfile.rails7.0.2.2
```

# TODOs
* Rebuild  the image before perform `bundle install` (or just remove the image, docker-compopse will build it automatically)
* Make sure the web container is running, need to fix this error: A server is already running. Check /app/tmp/pids/server.pid.
