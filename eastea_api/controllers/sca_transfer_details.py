from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger
from odoo import http


class SCAStockTransfer(http.Controller):
    @http.route('/data/SCA/GetStockTransfer1', type='json', csrf=False, auth='public')
    def SCAStockTransfer(self):
        transfer_rec = request.env['stock.picking'].sudo().search(
            [('location_dest_id.name', 'like', 'Route'), ('state', '=', 'done')])
        transfer = []
        for rec in transfer_rec:
            order_line = []
            # for l in rec.move_ids_without_package:
            #
            #     order_line.append({
            #         'Product name':l.product_id.name,
            #         'Price':l.price,
            #     })
            for line in rec.move_line_ids_without_package:
                order_line.append({
                    'Product_line_id': line.id,
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'product_code': line.product_id.default_code,
                    'lot_number': line.lot_id.name,
                    'consumed_qty': line.qty_done,
                    'price': line.move_id.price,
                    # 'Price list Price': l.price,
                    'unit_of_measure': line.product_uom_id.name
                })
            vals = {
                'Master_line_id': rec.id,
                'Transfer_id': rec.name,
                'Transfer_name': rec.picking_type_id.name,
                'destination_location': rec.location_dest_id.name,
                # 'Destination_location_code': rec.dest_loc_code,
                'source_location': rec.location_id.name,
                # 'Source_location_code': rec.so_loc_code,
                'date_done': rec.date_done,
                'line_items': order_line,
                # 'price': rec.price,

            }
            transfer.append(vals)
        data = {'status': 200, 'response': transfer, 'message': 'Done. All Products Returned'}
        return data
