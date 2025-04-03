class Model():
    def select(self):
        """
        Gets all rows from the "Bookmarked Internships" database.
        Each row contains: internship_title, organization, date_posted, location, internship_url, date_applied, application_status
        :return: List of lists containing all rows of database
        """
        pass

    def insert(self, new_entry: dict):
        """
        Inserts an entry into the "Bookmarked Internships" database.

        :new_entry (dict): A dictionary object containing information about the internship posting to be added.

        :return: True if an entry was added to the database. False if there already exists a row in the database with the same internship url as the entry to be added.
        :raises: Database errors on connection and insertion
        """
        pass

    def delete(self, internship_url: str):
        """
        Deletes an entry from the "Bookmarked Internships" database based on the provided internship url.

        :param internship_url (str): The url of the bookmarked internship posting to be removed.

        :return: True if a row was actually removed. False, otherwise.
        """
        pass

    def update(self, internship_url: str, attribute: str, value):
        """
        Updates a specific attribute of an entry from the "Bookmarked Internships" database.
        on the provided internship url.

        :param internship_url (str): The url of the bookmarked internship posting to be updated.
        :param attribute (str): The name of the attribute(column) in the table to be updated.
        :param value (str): The new value 

        :return: True 
        """
        pass

