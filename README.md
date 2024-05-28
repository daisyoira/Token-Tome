<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

# COMP6002 Project: Token Tome
<!-- ABOUT THE PROJECT -->
## About The Project

This project provides a copyright enforcement 
solution for digital libraries by watermarking 
and password protecting digital resources being
borrowed from the libraries.


### Built With

* Django (Python)
* Docker
* FPDF
* pypdf


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Docker https://docs.docker.com/desktop/install/windows-install/  


### Installation

1. Clone the repo.
   ```sh
   git clone https://github.com/daisyoira/Token-Tome.git
   ```
2. Install all the required packages in the requirements.txt
file.

3. Navigate to the directory with the compose.yaml.

4. Run the following command to start up the database
in the background.
   ```sh
   docker compose up --detach
   ```
   
5. In the same directory, create the database tables 
by running the following commands in the following order.
   ```sh
    python manage.py makemigrations
    python manage.py migrate  
   ```
   
6. Start the application server with following command.
   ```sh
   python manage.py runserver
   ```

7. Proceed to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use 
the application.

8. To check out the API documentation, use the api endpoint [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)

9. With the server running, run all the tests in the test.py file using the following command
   ```sh
   python manage.py test
   ```
10. Run the load test with a variable number of concurrent users using the locust command.
This provides a web interface where the total number of users can be specified. Provide the url http://localhost:8000
   ```sh
   locust 
   ```
<!-- CONTACT -->
## Contact

Daisy Oira

Project Link: [https://github.com/daisyoira/Token-Tome.git](https://github.com/daisyoira/Token-Tome.git)