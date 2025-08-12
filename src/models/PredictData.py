from src.server.main import db,main_app
from src.config.database import generateDatabase

class predict_data(db.Model):
  __tablename__ = 'predict_data'
  
  id = db.Column(db.Integer, primary_key=True)
  child_id = db.Column(db.Integer, nullable=False)
  parent_id = db.Column(db.Integer, nullable=False)
  url = db.Column(db.String(255), nullable=False)
  label = db.Column(db.String(255), nullable=False)
  
  def __init__(self, child_id, parent_id, url, label):
    self.child_id = child_id
    self.parent_id = parent_id
    self.url = url
    self.label = label
