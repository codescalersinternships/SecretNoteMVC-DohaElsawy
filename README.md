# Secret Note MVC 
Web application that allows users to securely share self-destructing secret notes.

## Installation 
- Download project
```py
    $ git clone https://github.com/codescalersinternships/SecretNoteMVC-DohaElsawy.git
    $ cd SecretNoteMVC-DohaElsawy
```
- Create a virtual environment to install dependencies in and activate it:
```py
  $ python -m venv .venv
  $ source .venv/bin/activate
```
- install the dependencies:
```py
  (.venv)$ pip install -r requirements.txt
```

### Setup your Environment variables:
```py
ENCRYPTKEY="example"  # this is the key encryption key for secure saving notes 
IP="0.0.0.0"     # choose your ip or put the ip of your container
PORT="8000"       # choose your exposed port 
CACHELOCATION="memcached"  # choose where is your memcached location, leave it empty for localhost location
```
### Interacte with application:
- `` make up `` establish the app
- `` make down `` shuts the app
- `` make all-migration`` run the required migrations
- `` make test `` run unit tests and migration tests
> [!WARNING]
> you have to leave `CACHELOCATION` ENV empty so that can run test locally


