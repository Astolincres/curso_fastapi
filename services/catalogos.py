from services.main import AppService

from utils.service_result import ServiceResult

from daos.catalogos_dao import CatalogosCRUD

from utils.app_exceptions import AppException

class CatalogosService(AppService):

    def pais_by_codigo(self, codigo) -> ServiceResult:
        pais = CatalogosCRUD(self.db).pais_by_codigo(codigo)
        if (not pais):
            return ServiceResult(AppException.GetPais({'detail': f'El pais {codigo} no existe'}))
        return ServiceResult(pais)