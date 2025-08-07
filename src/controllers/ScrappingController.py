
from flask import Blueprint
from flask import request,g
from src.services.ScrappingServices import ScrappingService
import src.utils.getResponse as Response  

ScrappingApp = Blueprint('ScrappingApp', __name__,)
scrappingService =  ScrappingService()

@ScrappingApp.route('/', methods=['GET'])
def index():
  return Response.success('',"success get all scrapping")

@ScrappingApp.route('/url', methods=['POST'])
def store():
  result = scrappingService.createCategory(request.json)
  if(result['status'] == 'failed'):
    return Response.error(result['data'],result['code'])
  
  return Response.success(result['data'],"success create new event")
