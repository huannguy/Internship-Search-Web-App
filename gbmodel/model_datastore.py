from .Model import Model
from datetime import datetime
from google.cloud import datastore

def from_datastore(entity):
    """
    Translates Datastore results into a dictionary format.

    :param entity: A datastore entity object.

    Datastore typically returns:
    [Entity{key: (kind, id), prop: val, ...}]

    return: [ internship_title, organization, date_posted, location, internship_url ]
    where internship_title, organization, location, and internship_url are Python strings
    and where date_posted is a Python datetime
    """
    if not entity:
        return None

    #Checks if entity is a list.
    if isinstance(entity, list):
        entity = entity.pop()   #Removes the last element in entity if it is a list.

    return [entity['internship_title'],entity['organization'],entity['date_posted'],entity['location'],entity['internship_url'],entity['date_applied'],entity['application_status']]

class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-nguyen-huannguy')

    def select(self):
        """
        Fetches all rows from the "BookmarkedInternships" kind in the datastore.

        Each row in the kind "BookmarkedInternships" contains: 
        - internship_title     (The title of the internship)
        - organization         (The organization offering the internship)        
        - date_posted          (The date the internship was posted)
        - location             (The location of the organization)
        - internship_url       (The url to the internship posting) 
        - date_applied         (The date the user applied for the internship position) 
        - application_status   (The current status of their application ('Not Yet Applied', 'Accepted', 'Pending', or 'Rejected')) 

        :return: List of dictionaries, where each dictionary represents a row in the datastore.
        """
        #Cretes a query for the 'BookmarkedInternships' kind.
        query = self.client.query(kind = 'BookmarkedInternships')

        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self, new_entry: dict):
        """
        Inserts an entry into the "bookmarked_internships" kind.
        :new_entry (dict): A dictionary object containing information about the internship posting to be added.

        :return: True if an entry was added to the database. False if there already exists a row in the database with the same internship url as the entry to be added.
        :raises: Database errors on connection and insertion
        """

        #Tracks whether the insertion was successful.
        was_added = False
       
        #Creates a new key for the 'Songbook' kind.
        key = self.client.key('BookmarkedInternships', new_entry['internship_url'])

        #Attempts to retrieve a row with the same internship url as the entry to be added, 
        entity = self.client.get(key)

        #If there are no rows with the same internship url...
        if entity == None: 
            #Creates a new entity and populates it with data.
            new_entity = datastore.Entity(key)
            new_entity.update({
                'internship_title':new_entry['internship_title'], 
                'organization':new_entry['organization'], 
                'date_posted':new_entry['date_posted'], 
                'location':new_entry['location'], 
                'internship_url':new_entry['internship_url'], 
                'date_applied':new_entry['date_applied'], 
                'application_status':new_entry['application_status']
            })

            was_added = True
            
            #Saves the entity into the datastore.
            self.client.put(new_entity)

        return was_added

    def delete(self, internship_url: str):
        """
        Removes an entry from the "BookmarkedInternships" kind given
        a specific url.

        :param internship_url (str): The url of the bookmarked internship posting to be updated.

        :return: True
        """ 
        #Create a key for the entity using the internship_url as the identifier
        key = self.client.key('BookmarkedInternships', internship_url)

        #Remove the entity from the datastore.
        self.client.delete(key)
        return True

    def update(self, internship_url: str, attribute: str, value):
        """
        Updates a specific attribute of an entry from the "bookmarked_internships" kind based
        on the provided internship url.

        :param internship_url (str): The url of the bookmarked internship posting to be updated.
        :param attribute (str): The name of the attribute(column) in the table to be updated.
        :param value (str): The new value 

        :return: True if a row was actually changed. False, otherwise.
        """

        was_updated = False

        #Create a key for the entity using the internship_url as the identifier
        key = self.client.key('BookmarkedInternships', internship_url)

        #Retrieve the entity from Datastore
        entity = self.client.get(key)

        if entity != None:
            entity[attribute] = value   #Update the specified property with the provided value
            self.client.put(entity)    #Save the updated entity back to Datastore
            was_updated = True

        return was_updated
