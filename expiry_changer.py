import datetime
import socket
import xmlrpc.client

class DataBaseTools:
    def __init__(self,url,db,username,password):

        self.url = url
        self.db = db
        self.username = username
        self.password = password

        self.change_expiration_date()

    def connect(self):
        try:
            # Set the socket timeout to 10 seconds
            timeout = 10
            socket.setdefaulttimeout(timeout)

            common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(self.url))
            self.models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self.url))
            # Authenticate the user
            self.uid = common.authenticate(self.db, self.username, self.password, {})
            print(f"Conectado a la base de datos {self.db}")
        
        except socket.timeout:
            print(f"Error al conectarse a la base de datos {self.db}")
            
        except Exception as e:
            print(f"Error al conectarse a la base de datos {self.db}")
            print(e)
            
    def change_expiration_date(self):

        # Connect to the database
        self.connect()

        # Get the current date and add 30 days
        date = datetime.date.today() + datetime.timedelta(days=30)
        date = date.strftime("%Y-%m-%d")

        target_model = 'ir.config_parameter'
        # Search for the record with key = 'database.expiration_date'
        record_id = self.models.execute_kw(self.db, self.uid, self.password, target_model, 'search',[[['key', '=', 'database.expiration_date']]])   
        # update the record with the new date
        update = self.models.execute_kw(self.db, self.uid, self.password, target_model, 'write',[record_id, {'value': date}])

        if update:
            print(f"{self.db} Se actualizó el registro con la fecha {date}")
        else:
            print("No se actualizó el registro")