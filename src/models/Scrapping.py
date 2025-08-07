from src.server.main import db,main_app
from src.config.database import generateDatabase
class Scrapping(db.Model):
  __tablename__ = 'scrapping'
  
  Scrapping_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), unique=True)
  
  def __init__(self,name ):
    self.name = name
  