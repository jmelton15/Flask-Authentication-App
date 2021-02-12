<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

# Flask-Auth Application
* Simple User Account Authentication and Authorization Full-Stack Application
* Allows a User to create an account and post feedback on the site
* Server side authentication and authorization is in place to only allow that user to access their account
  as well as only allow that user to edit/delete their own feedback posts
* Implemented password encryption for safe storage of the user information in a postgreSQL database
* Also implemented a mail server using gmail SMTP which allows a user to reset their password
* The password reset is handled with url_safe tokens server side


### Built With - Credits To The Following:

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [postgreSQL](https://www.postgresql.org/)
* [SQL-Alchemy](https://www.sqlalchemy.org/)
* [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-WTForms](https://flask-wtf.readthedocs.io/en/stable/)
* [HTML & CSS]
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
* [Bootstrap 5](https://getbootstrap.com/)
* [GMAIL](https://google.com)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps follow the Prerequisites and Installation steps
Then follow these next three:
*First, you can ignore the google-api installs in the requirements.text
* Second, you will need your own virtual environment in python and workspace (I used visual studio code)
* Third, you will need to install the following from installation list
* Fourth, I added a sample_config.py file so you can add in your secrets in a way that will function with the code
  Rename this file back to config.py so it will work with the code


### Prerequisites

* You will need Python 3.7 or later
  ```sh
  https://www.python.org/downloads/
  ```
* You will need Flask and Flask-sqlalchemy, which you can get in one pip install
* You will need to create a postgreSQL database called authenticate in order to use this application
* However, if you know where to change the database you are using, you can name your database anything


### Installation

1. FYI - I used GIT BASH as my shell and terminal

2. If you don't already have Python 3.7 or later
   ```sh
   https://www.python.org/downloads/
   ```
3. Clone the Repo 
   ```sh
   git clone git@github.com:jmelton15/Flask-Authentication-App.git
   ```
4. Install pre-req for flask-sqlalchemy
   ```sh
   pip install psycopg2-binary
   ```
5. Install Flask and Flask-sqlalchemy using pip.. this will get both in one install
   ```
   pip install flask-sqlalchemy
   ```
6. Install flask WTForms
   ```sh
   pip install flask-wtf
   ```
7. Install python requests
   ```sh
   pip install requests
   ```
8. Install flask Bcrypt
   ```sh
   pip install flask-bcrypt
   ```
9. Install pyautogui (for message box capabilities)
   ```sh
   pip install pyautogui
   ```
10. Create a postgreSQL database called authenticate
   While in the psql: terminal input the following code
   ```sh
   CREATE DATABASE authenticate (or whatever name you choose);
   ```
11. To run the server with flask - the following should do the trick
   ```
   flask run
   ```

<!-- CONTACT -->
## Contact

Your Name - [John Melton]

Project Link: [https://github.com/jmelton15/Flask-Authentication-App](https://github.com/jmelton15/Flask-Authentication-App)

