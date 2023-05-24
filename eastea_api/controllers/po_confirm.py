from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _




class PoConfirm(http.Controller):

    @http.route('/po_confirm', type='json', csrf=False, auth='public')
    def po_confirm(self, **rec):
        for row in rec["data"]:
            ponumber = row["ponumber"]
            po = request.env['purchase.order'].sudo().search([('name', '=', ponumber)]) or False
            for rec in po:
                rec.button_confirm()
                rec.button_unlock()
            # rec.state = "cancel"