
from src.repositories.CleanDataRepository import CleanDataRepository
from src.repositories.PredictDataRepository import PredictDataRepository
from src.utils.convert import queryResultToDict
from src.services.Service import Service
from src.utils.errorHandler import errorHandler
import os # Pastikan os diimpor
cleanDataRepository = CleanDataRepository()
predictDataRepository = PredictDataRepository()

class HITLService(Service):
    @staticmethod
    def failedOrSuccessRequest(status, code, data):
        return {
            'status': status,
            "code": code,
            'data': data,
        }

    def updatePredictLabelById(self, predict_id, new_label):
        try:
            # Validasi dan proses data di sini
            updated_predict_data = predictDataRepository.updatePredictLabelById(predict_id, new_label)
            if not updated_predict_data:
                return self.failedOrSuccessRequest('failed', 404, 'Data tidak ditemukan')
            return self.failedOrSuccessRequest('success', 200, 'Data berhasil diperbarui')
        except Exception as e:
            return self.failedOrSuccessRequest('failed', 500, str(e))