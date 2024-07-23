# flask Basic

## Setup
### step 0 Install Python

### step 1 Python install virtual environments packages (for create environments)
pip install virtualenvwrapper-win

### step 2 Python create virtual environments
mkvirtualenv flask_server_betask_linked

### step 3 Python work on virtual environments
workon flask_server_betask_linked

### step 4 Python install packages in virtual environments
* pip install -r requirements.txt

> if have list packages in requirements.txt file
* pip install _{Name packages}_


## Start project flask
### step 1 Python work on virtual environments
workon _{Name virtual environments}_

### step 2 Run Python
* python app.py
* flask run
> if SET environments flask

### ADD LIB
brew install unixodbc
brew install freetds



### MAC SET First System
pip3 install virtualenv
virtualenv flask_server_betask_linked
source flask_server_betask_linked/bin/activate
pip3 install -r requirements.txt
python3 app.py

### MAC Start project 
source flask_server_betask_linked/bin/activate
python3 app.py



### DOCKER build and complie 

docker build -t registry.gitlab.com/v.group-honda/betask-linked .
docker push registry.gitlab.com/v.group-honda/betask-linked
docker run --name flask_core -i -d -p 5001:5001 registry.gitlab.com/v.group-honda/betask-linked


# docker Delete
docker stop flask_core
docker rm flask_core
docker system prune -a