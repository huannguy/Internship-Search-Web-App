from flask import redirect, request, url_for, render_template, session, flash
from flask.views import MethodView
import requests
import gbmodel
import os

def fetch_internships(api_key: str, endpoint:str , max_results: int, title_filter: str = None, organization_filter: str = None, location_filter: str = None):
    """
    Retrieves the internship postings returned from the 'Internship API' in 
    batches until the desired number of results is reached or no more results is 
    available.

    :param api_key(str): The API key required for authentication.
    :param endpoint (str): The API endpoint URL from which to fetch internship postings.
    :param max_results (int): The maximum number of internship postings to retrieved.
    :param title_filter (str, optional): A keyword to filter internships by title (default: None).
    :param organization_filter (str, optional): A keyword to filter by organization name (default: None).
    :param location_filter (str, optional): A keyword to filter internships by location (default: None).

    :return: A list of dictionary objects
    """

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "internships-api.p.rapidapi.com"
    }

    #List object to hold the fetched internship entries.
    internships = []
    offset = 0         #The starting ppint for the batch of internships to fetch.
    batch_size = 10    #The default number of requests returned by the API per page.

    #Processes all results returned from the API.
    while len(internships) < max_results:
        params = {
            "offset": offset,
            "title_filter": title_filter,
            "organization_filter": organization_filter,
            "location_filter": location_filter
        }

        #Sends a GET request to the API with the specified headers and parameters
        response = requests.get(endpoint, headers=headers, params=params)

        #Checks if the response was successful (status code 200)
        if response.status_code != 200:
            print("Error fetching data:", response.json())  # Print error if the request fails
            break

        #Converts response data into a JSON object.
        data = response.json()

        #Breaks out of the loop if there are no more results.
        if not data:
            break  

        #Appends the list of internship entries to the running list.
        internships.extend(data)
        offset += batch_size

    #Return the requested number of internships (up to max_results)
    return internships[:max_results]

class Index(MethodView):
    def get(self):
        return render_template('index.html')

class Search(MethodView):
    def get(self):
        return render_template('search.html')
    
    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to display page when completed.
        """
        # Store the user-provided filter values in the session to persist across requests
        session['title_filter'] = request.form['title_filter']
        session['organization_filter'] = request.form['organization_filter']
        session['location_filter'] = request.form['location_filter']

        #Redirect the user to the 'display' page after the filters have been set
        return redirect(url_for('display'))
 
class Display(MethodView):
    def get(self):
        """
        Handles GET requests for displaying the internship postings returned by the API.
        Renders the 'display.html' template, passing the internship entries.
        """
        endpoint1 = "https://internships-api.p.rapidapi.com/active-ats-7d"
        endpoint2 = "https://internships-api.p.rapidapi.com/active-jb-7d"
        internships = []

        #Fetch internships from the API with the filters stored in the session.
        api_key = os.environ.get('INTERNSHIP_API_KEY')
        
        internships.extend(fetch_internships(api_key, endpoint1, 10, session.get('title_filter'), session.get('organization_filter'), session.get('location_filter')))
        internships.extend(fetch_internships(api_key, endpoint2, 10, session.get('title_filter'), session.get('organization_filter'), session.get('location_filter')))

        #Processes the fetched internships to remove the time part in the 'date_posted' field.
        for entry in internships:
            entry['date_posted'] = entry['date_posted'].split("T")[0]

        #Renders the 'display.html' template and passes the list of internships to it         
        return render_template('display.html', entries=internships)
    
    def post(self):
        """
        Handles POST requests for bookmarking internship postings returned by the API.
        Redirect to the display page when completed.
        """
        model = gbmodel.get_model()
        result = True

        #Checking whether the field internship_url is a non-empty string before calling the 
        #insert method to add the entry to the database.
        if request.form['internship_url']:
            new_entry = {
                "internship_title": request.form['internship_title'],
                "organization": request.form['organization'],
                "date_posted": request.form['date_posted'],
                "location": request.form['location'],
                "internship_url": request.form['internship_url'],
                "date_applied": None,
                "application_status": None
            }

            result = model.insert(new_entry)

        #Sends a flash message to the front-end if the entry to be added has the same internship endpoint as an existing entry in
        #database.
        if result == False:
            flash({'message': "This posting has already been bookmarked.", 'endpoint': request.form['internship_url']})

        return redirect(url_for('display'))

class ManualAdd(MethodView):
    def get(self):
        return render_template('manual-add.html')

    def post(self):
        """
        Handles POST requests for manually adding a new bookmarked internship entry.
        Redirect to the manage page when completed.
        """
        model = gbmodel.get_model()
        result = True

        #Checking whether the field internship_url is a non-empty string before calling the 
        #insert method to add the entry to the database.
        if request.form['internship_url']:
            new_entry = {
                "internship_title": request.form['internship_title'],
                "organization": request.form['organization'],
                "date_posted": request.form['date_posted'],
                "location": request.form['location'],
                "internship_url": request.form['internship_url'],
                "date_applied": None,
                "application_status": None

            }
            result = model.insert(new_entry)

        #Sends a flash message to the front-end if the entry to be added has the same internship endpoint as an existing entry in
        #database.
        if result == False:
            flash("There already exists an entry with that same endpoint")
            return redirect(url_for('manual-add'))

        return redirect(url_for('manage'))
 
class Manage(MethodView):
    def get(self):
        """
        Handles GET requests to the manage page.
        Renders the 'manage.html' template and passes the internship entries to it.
        """
        model = gbmodel.get_model()

        #Converts the data into a list of dictionaries.
        entries = [dict(internship_title=row[0], organization=row[1], date_posted=row[2], location=row[3], 
                            internship_url=row[4], date_applied=row[5], application_status=row[6]) for row in model.select()]

        #Renders the 'manage.html' template and passes the internship entries to it.
        return render_template('manage.html',entries=entries)

    def post(self):
        """
        Handles POST requests for managing bookmarked internships.
        Redirect to the manage page when completed.
        """
        model = gbmodel.get_model()
 
        #Checking if the selected operation is 'delete' and internship_url is not an empty string before 
        #attempting to remove the specified entry from the database.
        if request.form['operation'] == "delete" and request.form['internship_url'] != "":
            model.delete(request.form['internship_url'])

        #Checking if the selected operation is 'update' and internship_url is not an empty string before
        #attempting to update the 'date_applied' and/or 'application_status' fields.
        elif request.form['operation'] == "update" and request.form['internship_url'] != "":
            if request.form['date_applied'] != "":
                model.update(request.form['internship_url'], "date_applied", request.form['date_applied'])

            if request.form['new_status'] != "":
                model.update(request.form['internship_url'], "application_status", request.form['new_status'])

        return redirect(url_for('manage'))

