from src.models.PredictData import predict_data,db
from src.repositories.CleanDataRepository import CleanDataRepository

cleanDataRepository = CleanDataRepository()

class PredictDataRepository:
  def getAllPredictData(self):
    return predict_data.query.all()
  def createNewPredictData(self, data):
    new_predict_data = predict_data(
      child_id=data['child_id'],
      parent_id=data['parent_id'],
      log_id=data.get('log_id'),  #
      url=data['url'],
      label=data['label']
    )
    db.session.add(new_predict_data)
    db.session.commit()
    return new_predict_data


  def getPredictDataById(self, id):
    return predict_data.query.get(id)
  def getPredictDataByUrl(self, url):
    return predict_data.query.filter_by(url=url).first()
  
  def updatePredictLabelById(self, predict_id, new_label):
    predict_data_to_update = self.getPredictDataById(predict_id)
    if not predict_data_to_update:
      return None
    predict_data_to_update.label = new_label
    db.session.commit()
    return predict_data_to_update

  def updatePredictData(self, id, data):
    predict_data_to_update = predict_data.query.get(id)
    if not predict_data_to_update:
      return None
    predict_data_to_update.child_id = data['child_id']
    predict_data_to_update.parent_id = data['parent_id']
    predict_data_to_update.url = data['url']
    predict_data_to_update.label = data['label']
    db.session.commit()
    return predict_data_to_update

  def deletePredictData(self, id):
    predict_data_to_delete = predict_data.query.get(id)
    if not predict_data_to_delete:
      return None
    db.session.delete(predict_data_to_delete)
    db.session.commit()
    return predict_data_to_delete
  
  def deletePredictDataByUrl(self, url):
    predict_data_to_delete = self.getPredictDataByUrl(url)
    if not predict_data_to_delete:
      return None
    db.session.delete(predict_data_to_delete)
    db.session.commit()
    return predict_data_to_delete