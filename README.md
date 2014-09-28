jugger-ranking
==============

A web application to rank jugger teams based on the games they played.
At the moment it only has one ranking system (Fred's Completely Fair Jugger
Ranking).

The application is implemented on top of the [Django Web Framework](https://www.djangoproject.com/). Implementation and testing is currently done against Django 1.4 and Python 2.7, but should work with any later version as well.

How to install/test
-------------------

First of all, You will need to create a private settings file named `backend/juggerranking/settings\_private.py`. An example can be found in `backend/juggerranking/settings\_private.py.example`.
Then You can create/sync the database using `backend/manage.py syncdb`.
Finally, You can either run Django's built-in webserver by calling `backend/manage.py runserver` or configure Your favorite web server for Django.
