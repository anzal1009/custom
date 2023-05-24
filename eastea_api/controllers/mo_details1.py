from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time


class GetMODetails1(http.Controller):
    @http.route('/data/GetMODetails1', type='json', csrf=False, auth='public')
    def get_manufacture(self):
        mo_rec = request.env['mrp.production'].sudo().search([('state', '=', 'done')])
        mo_details = []
        for rec in mo_rec:

            order_lines = []
            for line in rec.move_raw_ids:
                for l in line.move_line_ids:
                    order_lines.append({
                        'consumed_product': l.product_id.name,
                        'consumed_qty': l.qty_done,
                        'lot':l.lot_id.name,
                        # 'done_qty':line.quantity_done
                    })
                print(order_lines)

            vals = {
                # 'id': rec.partner_id,
                'manufacturing_order_no': rec.name,
                'product_name': rec.product_id.name,
                'qty': rec.product_qty,
                # 'blend': rec.blend,
                # 'bom_id':rec.b,om_id.id,
                'date': rec.date_planned_start,
                'line_items': order_lines,
            }
            mo_details.append(vals)
        data = {'status': 200, 'response': mo_details, 'message': 'Done All Products M O Returned'}
        return data