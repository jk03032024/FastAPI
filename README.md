# MSDP

This repository contain MSDP APIs

To develop or test the APIs, we need docker installed and also git-bash terminal if it is not Linux flavored OS terminal.

## 

firstly change the volume paths metioned in compose.yml as per your system

## Useful commands
The **run.sh** is an absolute control point, where there are commands to run tests, run APIs and also applying DB migrations using Liquibase. Some of the useful command are

`>sh run.sh tests` This command will run tests and print test coverage for the code in `api` directory

`>sh run.sh tests NO_DB_SHUTDOWN` This will again run the tests and print test coverage report, but this time it will not shutdown the DB at the end. This is needed when you want to apply DB migration from feature branch to master branch, because that's what happen in prod after first release. So first checkout the master, run this command and than checkout the feature branch and run this command again to validate the liquibase will not throw any error on prod.

`>sh run.sh apis` This command will run fastapi sever exposing them on 127.0.0.1:8000

>If you see a **connection refused error** while using any of the above command, try again, sometimes the Postgres containeris not ready to accept the connections when liquibase or apis container are tryinn to connect.

>**Note:** In future any repetitive thing/command should be added in the `run.sh` and than run.sh should be used to save development time.
## Architecture
The local development IDE could be anything the developer likes. As we use docker-compose to manage the application and everything from APIs, Liquibase to Postgres are running as a container.


## To Run The Project On LINUX OS

use command 

`> sudo ./run.sh apis` in some linux system ./ does not works so you can use 
`> sudo bash run.sh apis` it will work on every linux flavour 