import datetime
import xmlrpc.client

class DataBaseTools:
    def __init__(self,url,db,username,password):

        self.url = url
        self.db = db

        self.username = username
        self.password = password

        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(self.url))
        self.models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self.url))
        # Authenticate the user
        self.uid = common.authenticate(self.db, self.username, self.password, {})

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