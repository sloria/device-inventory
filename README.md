
# Inventory Project #

## About ##

## Prerequisites ##

- Python >= 2.5
- pip
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

- Install prerequisites
- cd to inventory directory
- Optional: Edit compiled.txt to choose your database adapter. Skip this to use sqlite
- `$ pip install -r requirements/dev.txt`
- `$ cp inventory/settings/local-dist.py sepal/settings/local.py` (so that local.py won't be added
  to your source control)
- Edit local.py with your local database settings.
- `$ python manage.py syncdb`
-  Perform any necessary migrations
- `$ python manage.py runserver`


## Running tests ##
- Run tests using `$ fab test`
- In order to test sending email, you can create a dummy SMTP server using `$ python -m smtpd -n -c DebuggingServer localhost:1025`


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
