from src.models.CleanData import clean_data,db

class CleanDataRepository:
  def getAllCleanData(self):
    return clean_data.query.all()  
  def getCleanDataByUrl(self, url):
    return clean_data.query.filter_by(url=url).first()
  
  def createNewCleanData(self,data):
    required_keys = {'url', 'text', 'stopword_removed_tokens'}
    if not required_keys.issubset(data.keys()):
        raise ValueError(f"Data tidak lengkap untuk membuat CleanData. Butuh: {required_keys}")

    new_clean_data = clean_data(
        url=data['url'],
        text=data['text'],
        raw_text=data['raw_text'],
        stopword_removed_tokens=data['stopword_removed_tokens'],
        link_gambar=data['link_gambar'],
        folder_gambar=data['folder_gambar']
    )
    db.session.add(new_clean_data)
    db.session.commit()
    return new_clean_data

  def getCleanDataById(self,clean_data_id):
    return clean_data.query.filter_by(clean_data_id=clean_data_id).first()

  def updateCleanData(self,id,data):
    clean_data = clean_data.query.filter_by(clean_data_id=id).first()
    if(not clean_data) :return False
    clean_data.name = data['name']
    db.session.commit()
    return clean_data

  def deleteCleanData(self,id):
    clean_data = clean_data.query.filter_by(clean_data_id=id).first()
    if(not clean_data) :return False
    db.session.delete(clean_data)
    db.session.commit()
    return True
  def getCleanDataByName(self,name):
    return clean_data.query.filter_by(name=name).first()