# Rails on Docker
Tools and Docker images to make a fast Ruby on Rails development environment. With the production templates, moving from development to production will be seamless.

# Installation

# Usage

## Create a New Rails Project
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

## Using Rails Generator
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
