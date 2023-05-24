from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger
from odoo import http
from odoo.http import request


class MoDateConfirm(http.Controller):
    @http.route('/data/date',type='json', csrf=False, auth='public')
    def date(self, **rec):
        for row in rec["data"]:
            monumber = row["monumber"]
            mo = request.env['mrp.production'].sudo().search([('name', '=', monumber)]) or False
            for rec in mo:
                print(rec.product_id.name)
