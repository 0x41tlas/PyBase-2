from app import config
import psycopg2
import json

class Connect:

    def __init__(self, password):

        self.password = password
        self.database = None
        self.cursor = None

    def connect(self):
        """
        Connect method:
        Creates a connection to the database using paramiters in config.py, and creats a cursor object.
        """

        self.database = psycopg2.connect(
            database=config.database,
            user=config.user,
            password=self.password,
            host=config.host,
            port=config.port
        )

        self.cursor = self.database.cursor()

        return self.database, self.cursor

    def retrieve(self, query):
        """
        Retrieve method:
        Retrieves data using pre-determined query.
        """

        self.cursor.execute("""SELECT * FROM parts WHERE
        locate ~* (%s) OR
        item ~* (%s) OR
        manufacturer ~* (%s) OR
        description ~* (%s);""", (query, query, query, query))
        return json.dumps(self.cursor.fetchall())

    def entry(self, entered_fields):
        """
        Entry method:
        Enters data into the database.
        """

        print(entered_fields)
        item, loc, desc, man, = entered_fields['partName'], entered_fields['locate'], entered_fields['description'], entered_fields['manufacturer']
        try:
            quan = int(entered_fields['quant'])
        except Exception as e:
            print("Error: {}".format(e))
            return json.dumps("Error: {}".format(e))
        self.cursor.execute("""INSERT INTO parts (item, locate, description, manufacturer, quantity) VALUES (%s, %s, %s, %s, %s)""", (item, loc, desc, man, quan))
        self.database.commit()
        return json.dumps("Success")

    def delete_entry(self, entry_id):
        self.cursor.execute("""DELETE FROM parts WHERE id = (%s)""", (entry_id,))
        self.database.commit()
        return json.dumps('Success')

if __name__ == '__main__':
    connect = Connect("my_pswrd")
    connect.connect()
    connect.retrieve()
