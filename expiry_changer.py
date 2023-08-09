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

        self.connect()

        # Obtiene la fecha actual y le suma 30 días
        date = datetime.date.today() + datetime.timedelta(days=30)
        date = date.strftime("%Y-%m-%d")

        target_model = 'ir.config_parameter'
        # Busca el id del registro con key = 'database.expiration_date'
        record_id = self.models.execute_kw(self.db, self.uid, self.password, target_model, 'search',[[['key', '=', 'database.expiration_date']]])   

        # actualiza el campo expiration_date de la tabla ir.config_parameter
        update = self.models.execute_kw(self.db, self.uid, self.password, target_model, 'write',[record_id, {'value': date}])

        if update:
            print(f"Se actualizó el registro con la fecha {date}")
        else:
            print("No se actualizó el registro")