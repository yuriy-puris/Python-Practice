from flask import render_template, request, redirect, make_response, jsonify, url_for
from models import XRate, ApiLog
import xmltodict
import api
from datetime import datetime
class BaseController():
    
    def __init__(self):
        self.request = request

    def call(self, *args, **kwds):
        try:
            return self._call(*args, **kwds)
        except Exception as ex:
            return make_response(str(ex), 500)
    
    def _call(self, *args, **kwds):
        raise NotImplementedError("_call")

class ViewAllRates(BaseController):
    
    def _call(self):
        xrates = XRate.select()
        return render_template('xrates.html', xrates=xrates)

class UpdateRates(BaseController):
    
    def _call(self, from_currency, to_currency):
        if not from_currency and not to_currency:
            self._update_all()
        elif from_currency and to_currency:
            self._update_rate(from_currency, to_currency)
        else:
            raise ValueError('No found from_currency and to_currency')
        return redirect('/xrates')

    def _update_all(self):
        xrates = XRate.select()
        for rate in xrates:
            try:
                self._update_rate(rate.from_currency, rate.to_currency)
            except Exception as ex:
                print(ex)   

    def _update_rate(self, from_currency, to_currency):
        api.update_rate(from_currency, to_currency)


class GetApiRates(BaseController):
    
    def _call(self, fmt):
        xrates = XRate.select()
        xrates = self._filter(xrates)
        print('test', xrates)
        if fmt == 'json':
            return self._get_json(xrates)
        elif fmt == 'xml':
            return self._get_xml(xrates)
        raise ValueError(f'Unknow fmt: {fmt}')


    def _filter(self, xrates):
        args = self.request.args
        
        if 'from_currency' in args:
            xrates = xrates.where(XRate.from_currency == args['from_currency'])
        if 'to_currency' in args:
            xrates = xrates.where(XRate.to_currency == args.get('to_currency'))
        return xrates


    def _get_xml(self, xrates):
        d = {
                "xrates": {
                    "xrate": [
                        {
                            "from": rate.from_currency,
                            "to": rate.to_currency,
                            "rate": rate.rate
                        }
                        for rate in xrates
                    ]
                }
            }
        return make_response(xmltodict.unparse(d), {'Content-Type': 'text/xml'})
    
    def _get_json(self, xrates):
        return jsonify([{"from": rate.from_currency, "to": rate.to_currency, "rate": rate.rate} for rate in xrates])


class EditRate(BaseController):
    def _call(self, from_currency, to_currency):
        if self.request.method == 'GET':
            return render_template('rate_edit.html', from_currency=from_currency, to_currency=to_currency)

        if 'new_rate' not in request.form:
            raise Exception('new_rate parametr is required')
        if not request.form['new_rate']:
            raise Exception('new_rate must be not empty')
        
        update_count = (XRate.update(
                        { XRate.rate: float(request.form['new_rate']),
                          XRate.updated: datetime.now() }
                       ).where(XRate.from_currency == from_currency,
                               XRate.to_currency == to_currency).execute()
                       )
        return redirect(url_for('view_rates'))

class ViewLogs(BaseController):
    def _call(self):
        page = int(self.request.args.get('page', 1))
        logs = ApiLog.select().paginate(page, 10).order_by(ApiLog.id.desc())
        return render_template('logs.html', logs=logs)


