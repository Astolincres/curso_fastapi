from services.main import AppCRUD

class Historical(AppCRUD):

    def historical(self, data, modelo, accion, user_id: int):
        data = data.__dict__
        json = {}
        for key in data:
            if (key not in ['_sa_instance_state']):
                json[key] = data[key]
        json['history_type'] = accion
        json['history_user_id'] = user_id
        modelo = modelo(**json)
        self.db.add(modelo)
        self.db.commit()