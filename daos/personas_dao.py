from services.main import AppCRUD

from models.pais import PaisDB
from models.persona import PersonaDB

from daos.historical_dao import Historical

from utils.enums import typeHistorial

from datetime import datetime

class PersonasCRUD(AppCRUD):

    def crear_persona(self, item) -> PersonaDB:
        personas = PersonaDB(
            nombre = item.nombre,
            telefono = item.telefono,
            codigo_postal = item.codigo_postal,
            pais_nacimiento_id = item.pais_nacimiento
        )
        self.db.add(personas)
        self.db.commit()
        self.db.refresh(personas)
        # Historical(self.db).historical(personas, HistoricalPersonaDB, typeHistorial.ADD.value, user.id)
        return personas

    def get_persona(self, id) -> PersonaDB:
        return self.db.query(
            PersonaDB.nombre,
            PersonaDB.telefono,
            PersonaDB.codigo_postal,
            PaisDB.pais.label("pais_nacimiento")
        ).filter(
            PersonaDB.id == id,
            PersonaDB.deleted == None
        ).join(
            PaisDB,
            PaisDB.id == PersonaDB.pais_nacimiento_id,
            isouter = True
        ).first()

    def actualizar(self, id, item) -> PersonaDB:
        persona = self.db.query(PersonaDB).filter(PersonaDB.id == id).first()
        persona.nombre = item.nombre
        persona.telefono = item.telefono
        persona.codigo_postal = item.codigo_postal
        persona.pais_nacimiento_id = item.pais_nacimiento
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        # Historical(self.db).historical(persona, HistoricalPersonaDB, typeHistorial.UPDATE.value, user.id)
        return persona

    def eliminar(self, id):
        persona = self.db.query(PersonaDB).filter(PersonaDB.id == id).first()
        persona.deleted = datetime.now()
        self.db.add(persona)
        self.db.commit()
        self.db.refresh(persona)
        # Historical(self.db).historical(persona, HistoricalPersonaDB, typeHistorial.DEL.value, user.id)
        return persona