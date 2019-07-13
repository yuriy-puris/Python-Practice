from functools import wraps
from flask import request, render_template

from app import app
import controllers
from config import IP_LIST

def check_IP(func):
    @wraps(func)
    def checker(*args, **kwds):
        if request.remote_addr not in IP_LIST:
            return abort(403)
        
        return func(*args, **kwds)
    
    return checker

@app.route('/')
def hello():
    return 'Hello everybody'

@app.route('/xrates')
def view_rates():
    return controllers.ViewAllRates().call()

@app.route('/api/xrates/<fmt>')
def api_rates(fmt):
    return controllers.GetApiRates().call(fmt)

@app.route('/update/<int:from_currency>/<int:to_currency>')
@app.route('/update/all')
def update_rates(from_currency=None, to_currency=None):
    return controllers.UpdateRates().call(from_currency, to_currency)

@app.route('/edit_rate/<int:from_currency>/<int:to_currency>', methods=['GET', 'POST'])
@check_IP
def edit_rate(from_currency, to_currency):
    return controllers.EditRate().call(from_currency, to_currency)
 
@app.route('/logs')
@check_IP
def view_logs():
    return controllers.ViewLogs().call()