[![Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](https://github.com/DestroyerAlpha/NC_CMRCET_KB141_PatanjaliHax/graphs/contributors)


# About the Project

## KB141_PatanjaliHax
Project by Team PatanjaliHax for the Problem Statement KB141 given by Government of Andhra Pradesh

### Built with
[Django](https://www.djangoproject.com/)
[Bootstrap](https://getbootstrap.com)


[Presentation](https://docs.google.com/presentation/d/1rpo1KZ37wxTqblmKbn9mhnkT26JYccbN5ZRfAkgsz08/edit?usp=sharing)

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



![profile](https://user-images.githubusercontent.com/46635452/89172684-a3559500-d5a0-11ea-940c-c3b63cf63f6e.png)

![profile](https://user-images.githubusercontent.com/46635452/89173672-44911b00-d5a2-11ea-8d68-da85497d8b53.png)
