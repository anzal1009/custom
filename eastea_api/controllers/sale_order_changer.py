from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class SaleOrderDate(http.Controller):
    @http.route('/data/sale/order', type='json', csrf=False, auth='public')
    def SaleOrder(self, **rec):

        so_numbers = []
        for row in rec["data"]:
            sale = row['so_no']
            invoice_date = row["date"]
            date = datetime.strptime(invoice_date, '%Y/%m/%d')
            sale_id = sale and request.env['sale.order'].sudo().search([('name', '=', sale)],limit=1) or False
            print(sale_id.date_order)
            sale_id.date_order = date
