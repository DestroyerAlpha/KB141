[![Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](https://github.com/DestroyerAlpha/NC_CMRCET_KB141_PatanjaliHax/graphs/contributors)


# About the Project

## KB141_PatanjaliHax
Project by Team PatanjaliHax for the Problem Statement KB141 given by Government of Andhra Pradesh

### Built with
[Django](https://www.djangoproject.com/)
[Bootstrap](https://getbootstrap.com)

### Installation Guide

Clone the repo using command
```
git clone https://github.com/DestroyerAlpha/NC_CMRCET_KB141_PatanjaliHax.git
```

Navigate to the directory NC_CMRCET_KB141_PatanjaliHax/portal/ and open the terminal
Setup the database tables using makemigrations and migrate command as below and createsuper user.
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
type the username and password in the terminal.

And finally start the server using the command
```
Python manage.py runserver 
```

Download the file media/papers/restricted.pdf  
open the admin page and login using super user credentials   
Create an user and add tags into appropriate tables.  
Add the restricted.pdf in research paper table and add the id of the restricted.pdf feed/views.py PaperPostCreateView class.  

