from services.main import AppCRUD

from models.pais import PaisDB

class CatalogosCRUD(AppCRUD):

    def pais_by_codigo(self, codigo):
        return self.db.query(
            PaisDB.id
        ).filter(
            PaisDB.codigo == codigo
        ).first()