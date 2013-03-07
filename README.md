# A simple device inventory #

## About ##
A simple Django app for device asset management.

## Prerequisites ##

- Python >= 2.5
- pip
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

- Install prerequisites
- cd to inventory directory
- Optional: Edit compiled.txt to choose your database adapter. Skip this to use sqlite
- `$ pip install -r requirements/dev.txt`
- `$ cp inventory/settings/local-dist.py inventory/settings/local.py` (so that local.py won't be added
  to your source control)
-  Edit local.py with your local database settings (only if using something other than sqlite).
- `$ python manage.py syncdb`
-  Perform any necessary migrations
    - e.g. `$ python manage.py migrate devices`
- `$ python manage.py runserver`

## Running tests ##
- Run tests using `$ fab test`
- To use watchdog (for CI), `$ ./bin/watchmedo.sh`.

License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
