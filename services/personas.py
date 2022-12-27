from services.main import AppService

from utils.service_result import ServiceResult

from daos.personas_dao import PersonasCRUD

from services.catalogos import CatalogosService

from utils.service_result import handle_result
from utils.app_exceptions import AppException

class PersonasService(AppService):

    def validar(self, item) -> ServiceResult:
        if (item.edad <= 18):
            return ServiceResult(AppException.Persona({'detail': f'Debe de ser mayor a 18 años'}))
        pais = handle_result(CatalogosService(self.db).pais_by_codigo(item.pais_nacimiento))
        item.pais_nacimiento = pais.id
        return ServiceResult(item)

    def crear_persona(self, item) -> ServiceResult:
        item = handle_result(self.validar(item))
        PersonasCRUD(self.db).crear_persona(item)
        return ServiceResult({'msg': 'Creado exitosamente'})

    def get_persona(self, id) -> ServiceResult:
        persona = PersonasCRUD(self.db).get_persona(id)
        if (not persona):
            return ServiceResult(AppException.Persona({'detail': f'No existe la persona: {id}'}))
        return ServiceResult(persona)

    def actualizar(self, id, item) -> ServiceResult:
        handle_result(self.get_persona(id))
        item = handle_result(self.validar(item))
        PersonasCRUD(self.db).actualizar(id, item)
        return ServiceResult({'msg': 'Actualizado exitosamente'})

    def eliminar(self, id) -> ServiceResult:
        handle_result(self.get_persona(id))
        PersonasCRUD(self.db).eliminar(id)
        return ServiceResult({'msg': 'Eliminado exitosamente'})