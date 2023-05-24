from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time


class DateChangerMO(http.Controller):
    @http.route('/data/MO/Date', type='json', csrf=False, auth='public')
    def mo_dates(self, **rec):
        for row in rec["data"]:
            monumber = row["monumber"]
            date = row["date"]
            print(date)
            invoice_date = datetime.strptime(date, '%d/%m/%Y')
            print(invoice_date)

            mo = request.env['mrp.production'].sudo().search([('name', '=', monumber)]) or False
            for rec in mo:
                print(rec.date_planned_start)
                rec.date_planned_start = invoice_date