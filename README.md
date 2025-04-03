# Internship-Search-Web-App

## Overview
A simple web application, hosted with Flask, that allows users to search for live internship postings and bookmark the internships that interest them. 
Bookmarked internships are stored using Google Cloud Datastore and users have the ability to remove and edit bookmarked entries at
their discretion. Internship postings are retrieved via the "Internship API" from RapidAPI.

## Technologies Used
**Back-end**: Python
**Front-end**: Jinja2, HTML, CSS, JavaScript
**Database**: Google Datastore

## Running The Application (Locally)
1. Clone the repository

2. Set up a virtual environment (optional but recommended)

3. Install dependencies
   
   ``pip install -r requirements.txt``

4. Configure and specify the relevant Google Cloud project and bucket in Model/Model.py

5. Run the application 

   ``python app.py``

## Future Improvements
User authentication to allow each user to have their own saved list of bookmarked internship postings.
Allow users to search for bookmarked internship postings based on various fields.
