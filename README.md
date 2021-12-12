# VITHackathon
Steps to Run the code:
1. Create a project folder in VScode.
2. Open the folder and create virtual environment by running the command "python -m venv env" in the terminal.
3. Move app.py file, templates folder and static folder in the virtual environment created. 



1. The Project made by us is based on the Problem Statement :"Fake News Detection". The main goal of this project is to detect whether the entered news by the user is Either Real or Fake.

2. This is currently a Web Application and can be easily deployed into Android Application in the format of .apk .

3. The Frontend Framework of this Application is built on Cordova and the Backend on Flask. The Application also consists of a bot, Selenium which does the automation work in the backend. There is a MySQL database for Storing the Login Credentials of all the Users and For Maintaining the Database of the Captured Fake News

4. User Journey :
   i) The first time user of this application will have to register himself/herself. Once registered succesfully , user       needs to login and will be redirected to the Home Page.
  ii) The Home Page consists of 2 buttons : a)Fake News and b)Verify News.
 iii) Once the User opens Verify News button , he will be asked to enter the news which he/she wants to verify is either          fake or real. Once he/she enters the news and submits it, Our Application will clearly display whether the news             entered is Fake or Real in one sentence. Below it, all the news headline related to the entered news by the user            will be displayed.(The Selenium Bot takes the input news from the user and searches the news on "Google News"               Webpage , an authenticated source. Once the search is completed , the Bot then performs NLP and gives the output on         the frontend through Flask).
  iv) When the User clicks on the Fake News button , he/she will be shown all the Fake News captured by the Bot throughout       its complete runtime from all the Users of this Application.

5. This Application is Accurate , Simple , Easy to use , workable on all cross-platforms because of the combination of Cordova and Flask and most importantly contributes to the society by avoiding the unnecessary confusion and chaos created by the Fake News circulating BEFOREHAND.
