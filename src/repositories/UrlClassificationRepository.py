from src.models.UrlClassification import url_classification,db
from src.repositories.CleanDataRepository import CleanDataRepository

cleanDataRepository = CleanDataRepository()

class UrlClassificationRepository:
  def getAllUrlClassifications(self):
    return url_classification.query.all()
  def createNewUrlClassification(self, data):
    new_url_classification = url_classification(
      url=data['url'],
      label=data['label'],
      stopword_removed_tokens=data['stopword_removed_tokens']
    )
    db.session.add(new_url_classification)
    db.session.commit()
    return new_url_classification
  def getUrlClassificationById(self, id):
    return url_classification.query.get(id)
  def getUrlClassificationByUrl(self, url):
    return url_classification.query.filter_by(url=url).first()
  def updateUrlClassification(self, id, data):
    url_classification_to_update = url_classification.query.get(id)
    if not url_classification_to_update:
      return None
    url_classification_to_update.url = data['url']
    url_classification_to_update.label = data['label']
    db.session.commit()
    return url_classification_to_update

  def deleteUrlClassification(self, id):
    url_classification_to_delete = url_classification.query.get(id)
    if not url_classification_to_delete:
      return None
    db.session.delete(url_classification_to_delete)
    db.session.commit()
    return url_classification_to_delete
