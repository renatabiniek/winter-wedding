# Table of Contents 

1. [**Introduction**](#Introduction)
2. [**User Experience (UX)**](#User-Experience-(UX))
    * [Project goals](#Project-goals)
    * [Target audience](#Target-audience)
    * [User stories](#User-stories)
    * [Structure](#Structure)
    * [Design](#Design)

3. [**Features**](#Features)
    * [Existing Features](#Existing-Features)
    * [Features to be implemented in the future](#Features-to-be-implemented-in-the-future)

4. [**Technologies used**](#Technologies-used)

5. [**Deployment**](#Deployment)
    * [Deploying to Heroku](#Deploying-to-GitHub-Pages)
    * [Forking to GitHub Repository](#Forking-to-GitHub-Repository)
    * [Making a local clone](#Making-a-local-clone)

6. [**Testing**](#Testing)
    * [Testing Approach](#Testing-Approach)
    * [User stories testing from the UX section](#User-stories-testing-from-the-UX-section)
    * [Validator Testing](#Validator-Testing)
    * [Issues and Bugs](#Issues-and-Bugs)

7. [**Credits**](#Credits)

8. [**Acknowledgments**](#Acknowledgments)

9. [**Disclaimer**](#Disclaimer)

<br>

# Winter Wedding RSVP

[Live program](https://winter-wedding.herokuapp.com/)

<br>

## Introduction
---

Winter Wedding RSVP tool is a terminal based application that allows users to RSVP to a wedding invite they had received.
It works with Google Sheets to record and retrieve individual responses, as well as to calculate totals and return them to the admin of the application.
The data can then be used for further planning linked to the event.


## User Experience (UX)
---
### Project goals

* to provide a tool for wedding guests they can use to send their RSVP
* to record their responses in an organised data file
* to track and monitor responses submitted

### Target audience

* Specific group of guests and their families who had been invited to a wedding

### User stories:

* as an invited guest, I want to be able send my RSVP
* as an invited guest, I want to be able to see a confirmation of my responses
* as a user, I want to clearly understand what actions are required
* as a user, I want to be clearly notified about any errors during the RSVP process
* as a returning user, I want to be notified if my response had already been recorded and what it said
* as an admin of the tool, I want to be able to access overview of RSVPs received

### Structure:

* Flowchart

* Database Structure



### Design: 

As this is a terminal based application, the design is limited. 
I have kept the basic terminal colours and fonts as per the Code Institute's template used.
The only addition to the design is the intro logo shown when the program starts. It illustrates the purpose of the tool and entices the user to interact with it.

## Features
---

### Existing Features



### Features to be implemented in the future

* 

## Technologies used
---

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - language used for this project
* [Code Institute Template](https://github.com/Code-Institute-Org/python-essentials-template) - to display and run the command line terminal in the browser
* Google Sheets
* [Google Cloud Platform](https://console.cloud.google.com/)
* gsptread
* re
* google.oauth2.service_account
* datetime
* [Heroku](https://heroku.com/) - for presenting the deployed project
* [GitHub](https://github.com/) - for hosting the project code and version control 
* [Gitpod](https://gitpod.io/) - to write the code and push it to GitHub
* [PEP8 Online Validation Service](http://pep8online.com/) - to validate the code
* [Online-Spellcheck](https://www.online-spellcheck.com/) - to spellcheck the content of the site and README

## Deployment
---
### Deploying to Heroku

The project was developed in GitPod, committed to Git and pushed to GitHub. 
The site was deployed to Heroku with the following steps:

1. Login to Heroku
2. 
3. 
4. 
5. 

### Forking to GitHub Repository

You can create a fork (copy) of the repository. This allows you to experiment with the code without affecting the original project.

To fork the repository:

1. Log in to your [GitHub](https://github.com/) account 
2. On GitHub, navigate to the repository you want to fork
3. In the top right corner of the page, underneath your profile avatar, click **Fork**
4. You should now have a copy of the original repository in your GitHub account

### Making a local clone

You can clone your repository to create a local copy on your computer. Any changes made to the local copy will not affect the original project. To clone the **Winter Wedding** project, follow the steps below:

1. Log in to your [GitHub](https://github.com/) account and locate the [Winter Wedding repository](https://github.com/renatabiniek/winter-wedding)
2. In the repository, click on **Code** button located above all the project files
3. Under HTTPS, copy the link generated (https://github.com/renatabiniek/winter-wedding.git)
4. Open the terminal you're using, e.g. Gitpod
5. Change the current working directory to the location where you want the cloned directory created
6. Type ```git clone``` and then paste the URL you copied earlier:  
```git clone https://github.com/renatabiniek/winter-wedding.git``` 
7. Press **Enter** to create your local clone.

You can also refer to this [GitHub documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) for detailed instructions. 

## Testing
---

### Testing Approach

### User stories testing from the UX section

### Validator Testing

### Issues and Bugs

### Credits

* Love Sandwiches walk-through project by Code Institue has been used regulary as a reference when building this tool. Some code has been used and adjusted to fit the needs of this project.

* image for the welcome message taken from [Ascii Art](https://www.asciiart.eu/holiday-and-events/valentine)

* code to validate syntax of email address using regular expressions from [this article on Stackabuse](https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/)

* advice on how to split long regex from [this post on Stackoverflow](https://stackoverflow.com/questions/8006551/how-to-split-long-regular-expression-rules-to-multiple-lines-in-python/8006576#8006576)

### Acknowledgments

Thank you to:

My mentor Guido Cecilio for the invaluable support and feedback
The community on Slack
My partner for continous support

### Disclaimer

This program has been created for educational purposes only, as part of Code Institute’s Python Essentials Portfolio Project 3.
The requirements are to build a command-line application that allows your users to manage a common dataset.