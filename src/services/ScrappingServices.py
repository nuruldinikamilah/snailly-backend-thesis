
from src.repositories.ScrappingRepository import ScrappingRepository
from src.utils.convert import queryResultToDict
from src.services.Service import Service

from src.utils.errorHandler import errorHandler
scrappingRepository = ScrappingRepository()    

class ScrappingService(Service):
    @staticmethod
    def failedOrSuccessRequest(status, code, data):
        return {
            'status': status,
            "code": code,
            'data': data,
        }
    
    def getAllScrapping(self):
        try:
            data = scrappingRepository.getAllCategories()
            return scrappingRepository.failedOrSuccessRequest('success', 200, queryResultToDict(data))
        except Exception as e:
            return scrappingRepository.failedOrSuccessRequest('failed', 500, str(e))
    
    def createScrapping(self,data):
        try:
            newCategory = scrappingRepository.createNewCategory(data)
            return self.failedOrSuccessRequest('success', 201, queryResultToDict([newCategory])[0])
        except ValueError as e:
            return self.failedOrSuccessRequest('failed', 500, errorHandler(e.errors()))
        except Exception as e:
            return self.failedOrSuccessRequest('failed', 500, str(e))
        
    def updateCategory(self,id,data):
        try:
        
            event = scrappingRepository.getCategoryById(id)
            if not event:
                return self.failedOrSuccessRequest('failed', 404, 'Category not found')
            categoryUpdated = scrappingRepository.updateCategory(id,data)
            return self.failedOrSuccessRequest('success', 201, queryResultToDict([categoryUpdated])[0])
        except ValueError as e:
            return self.failedOrSuccessRequest('failed', 500, errorHandler(e.errors()))
        except Exception as e:
            return self.failedOrSuccessRequest('failed', 500, str(e))
        
    def deleteCategory(self,id):
        try:
            event = scrappingRepository.getCategoryById(id)
            if not event:
                return self.failedOrSuccessRequest('failed', 404, 'Event not found')
            
            scrappingRepository.deleteCategory(id)
            return self.failedOrSuccessRequest('success', 200, 'Event deleted')
        except ValueError as e:
            return self.failedOrSuccessRequest('failed', 500, errorHandler(e.errors()))
        except Exception as e:
            return self.failedOrSuccessRequest('failed', 500, str(e))