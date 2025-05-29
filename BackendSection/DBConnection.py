from dotenv import load_dotenv
import os
import pymysql
from BackendSection.House import House

# Load the environment variables
load_dotenv()

# This class handles the connection and interaction with the MySQL database
class DBConnection:
    def __init__(self):
        self.cursor = None
        try:
            # Connect to the MySQL database with your credentials
            self.db = pymysql.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )

            # Predefined SQL queries to use later
            self.select_all_query = """
                SELECT id, address1, address2, city, state, postal_code, country, photo, size, register_date FROM houses
            """
            self.select_by_id_query = "SELECT * FROM houses WHERE id=%s"
            self.insert_query = """
                INSERT INTO houses (id, address1, address2, city, state, postal_code, country, photo, size, register_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.update_query = """
                UPDATE houses 
                SET address1=%s, address2=%s, city=%s, state=%s, postal_code=%s, country=%s, 
                    photo=%s, size=%s, register_date=%s 
                WHERE id=%s
            """

            self.cursor = self.db.cursor()  # Creates a cursor to execute SQL commands
        except Exception as ex:
            print(ex)  # If something goes wrong, print the error

    # This function generates the next house ID like "H001", "H002", etc.
    def get_next_id(self):
        self.cursor.execute("SELECT id FROM houses ORDER BY id DESC LIMIT 1")  # Get the last inserted ID
        result = self.cursor.fetchone()

        if result:
            last_id = result[0]  # Example: "H005"
            num = int(last_id[1:]) + 1  # Take the number part and add 1
            return f"H{num:03}"  # Format it back into "H006", "H007", etc.
        else:
            return "H001"  # If no records exist yet, start at "H001"

    # Adds a new house to the database
    def add(self, house):
        try:
            self.cursor.execute(self.insert_query, house.get_insert_values())  # Insert house values
            self.db.commit()  # Save the changes to the database
            return 1, house.get_id()  # Return success and the ID
        except Exception as ex:
            print(f"[ERROR] Failed to insert house: {ex}")
            return 0, None  # Return failure

    # Gets all house records from the database
    def select_all_houses(self):
        self.cursor.execute(self.select_all_query)
        return self.cursor.fetchall()  # Returns a list of all rows

    # Finds and returns a specific house by its ID
    def select_by_id(self, house_id):
        values = (house_id,)  # Tuple with one item
        self.cursor.execute(self.select_by_id_query, values)
        result = self.cursor.fetchone()  # Get the matching row
        return House(*result) if result else None  # Return a House object or None if not found

    # Updates a house’s information in the database
    def update(self, house):
        self.cursor.execute(self.update_query, house.get_update_values())  # Run the update
        self.db.commit()  # Save the changes
        return self.cursor.rowcount  # Return how many rows were affected
    
    # Deletes a house via ID
    def delete(self, house_id):
        try:
            self.cursor.execute("DELETE FROM houses WHERE id = %s", (house_id,))
            self.db.commit()
            return self.cursor.rowcount  # returns 1 if a row was deleted
        except Exception as ex:
            print(ex)
            return 0



    # Closes the cursor and the database connection
    def close(self):
        self.cursor.close()
        self.db.close()