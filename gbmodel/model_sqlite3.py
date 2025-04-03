from datetime import date
from .Model import Model
import sqlite3
DB_FILE = 'bookmarked_internships.db'    # file for our Database

class model(Model):
    def __init__(self):
        #Checks if the database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        try:
            cursor.execute("select count(rowid) from bookmarked_internships")
        except sqlite3.OperationalError:
            cursor.execute("create table bookmarked_internships (internship_title text, organization text, date_posted text, location text, internship_url text, date_applied text, application_status text)")

        cursor.close()

    def select(self):
        """
        Gets all rows from the "bookmarked_internships" table

        Each row in the "BookmarkedInternships" table contains: 
        - internship_title     (The title of the internship)
        - organization         (The organization offering the internship)        
        - date_posted          (The date the internship was posted)
        - location             (The location of the organization)
        - internship_url       (The url to the internship posting) 
        - date_applied         (The date the user applied for the internship position) 
        - application_status   (The current status of their application ('Not Yet Applied', 'Accepted', 'Pending', or 'Rejected')) 

        :return: List of dictionaries, where each dictionary represents a row in the datastore.        
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookmarked_internships")
        return cursor.fetchall()

    def insert(self, new_entry: dict):
        """
        Inserts an entry into the "bookmarked_internships" table.
        :new_entry (dict): A dictionary object containing information about the internship posting to be added.

        :return: True if an entry was added to the database. False if there already exists a row in the database with the same internship url as the entry to be added.
        :raises: Database errors on connection and insertion
        """
        #Tracks whether the insertion was successful.
        was_inserted = False
        
        params = {
            'internship_title':new_entry['internship_title'], 
            'organization':new_entry['organization'], 
            'date_posted':new_entry['date_posted'], 
            'location':new_entry['location'], 
            'internship_url':new_entry['internship_url'], 
            'date_applied':new_entry['date_applied'], 
            'application_status':new_entry['application_status']
        }

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        #Checks if a row with the same internship url already exists in the database before attempting to insert a new row.
        cursor.execute("select exists(select 1 from bookmarked_internships where internship_url = ?)", (new_entry['internship_url'],))
        if cursor.fetchone()[0] == 0:
            was_inserted = True
                    
            cursor.execute("insert into bookmarked_internships (internship_title, organization, date_posted, location, internship_url, date_applied, application_status) "
                       "VALUES (:internship_title, :organization, :date_posted, :location, :internship_url, :date_applied, :application_status)", params)

        connection.commit()   #Commits the transaction to save changes.
        cursor.close()        #Closes the connection to the database.
        return was_inserted

    def delete(self, internship_url: str):
        """
        Deletes an entry from the "bookmarked_internships" table based on the provided internship url.
        
        :param internship_url (str): The url of the bookmarked internship posting to be removed.

        :return: True if a row was actually removed. False, otherwise.
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("delete from bookmarked_internships where internship_url=?", (internship_url,))

        #Returns False if no rows were removed.
        if cursor.rowcount == 0:
            return False
        
        connection.commit()   #Commits the transaction to save changes.
        cursor.close()        #Closes the connection to the database.

        return True
    
    def update(self, internship_url: str, attribute: str, value):
        """
        Updates a specific attribute of an entry from the "bookmarked_internships" table based
        on the provided internship url.

        :param internship_url (str): The url of the bookmarked internship posting to be updated.
        :param attribute (str): The name of the attribute(column) in the table to be updated.
        :param value (str): The new value 

        :return: True if a row was actually changed. False, otherwise.
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        #Updates the 'date_applied' attribute.
        if attribute == "date_applied":
            cursor.execute("UPDATE bookmarked_internships SET date_applied = ? WHERE internship_url = ?", (value, internship_url))

        #Updates the 'application_status' attribute.
        elif attribute == "application_status":
            cursor.execute("UPDATE bookmarked_internships SET application_status = ? WHERE internship_url = ?", (value, internship_url))

        #Returns False if no rows were changed.
        if cursor.rowcount == 0:
            return False

        #Otherwise, commit the change.
        connection.commit()
        cursor.close()

        return True