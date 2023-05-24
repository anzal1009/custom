from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time


class MoCreation(http.Controller):

    @http.route('/create_manufacturing_orders', type='json', auth='user')
    def create_manufacturing_orders(self, **rec):
        # print(rec)
        mo_number = []
        modetails = []
        move_raw_ids =[]
        for row in rec["data"]:
            for op in row["operation"]:
                op_type = op["op_type"]
                warehouse = op["warehouse"]

                if (warehouse == 'JOTHIPURAM'):
                    warehouse_data = warehouse and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                if (warehouse == 'KAVALANGAD'):
                    warehouse_data = warehouse and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

                if op_type:
                    op_type_id = op_type and request.env['stock.picking.type'].sudo().search(
                        [('name', '=', op_type)],
                        limit=1) or False



            for comp in row["rawmaterials"]:
                item_name = comp["product"]
                producing_qty = comp["qty"]
                source_loc = op_type_id.default_location_src_id
                dest_loc = op_type_id.default_location_dest_id

                if item_name:
                    item_id = item_name and request.env['product.product'].sudo().search(
                        [('name', '=', item_name)],
                        limit=1) or False


                move_raw_ids.append((0, 0, {
                    'product_id': item_id.id,
                    'name': "Mo Creation",
                    'product_uom_qty': producing_qty,
                    'location_id': source_loc.id,
                    'product_uom': item_id.uom_id.id,
                    'location_dest_id': dest_loc.id
                        }))

            for p in row["products"]:

                product_name = p["product"]
                quantity = p["qty"]
                shdate = p["date"]

                date = datetime.strptime(shdate, '%m/%d/%Y')
                if product_name:
                    product_id = product_name and request.env['product.product'].sudo().search(
                            [('name', '=', product_name)], limit=1) or False

                    modetails = request.env['mrp.production'].create({
                                'product_id': product_id.id,
                                'product_qty': quantity,
                                # 'qty_producing': product_qty,
                                'product_uom_id':  product_id.uom_id.id,
                                'date_planned_start': date,
                                # 'bom_id': bom_id.id,
                                'move_raw_ids': move_raw_ids,
                                'picking_type_id':op_type_id.id,
                                'location_src_id': source_loc.id,
                                'location_dest_id': dest_loc.id

                            })


                if modetails:
                    mo_number.append({
                        'M.O Number': modetails.name
                    })
                    modetails.action_confirm()
                    if modetails.move_raw_ids:
                        print("lines")
                        for lot in modetails.move_raw_ids:
                            for comp in row["rawmaterials"]:
                                item_name = comp["product"]


                                product = item_name and request.env['product.product'].sudo().search(
                                    [('name', '=', item_name)], limit=1) or False
                                if product:
                                    for line in lot.move_line_ids:
                                        product_lot = comp["lot"]
                                        lot_qty =comp["qty_done"]

                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('name', '=', product_lot),
                                             ('product_id', '=',item_name)])
                                        if not lot_no:
                                            print('lot_no lot_no')
                                            lot_number = {
                                                'name': product_lot,
                                                'product_id': product.id,
                                                'company_id':warehouse_data.id
                                            }
                                            create_lot_number = request.env['stock.production.lot'].sudo().create(
                                                lot_number)
                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('name', '=', product_lot)])
                                    line.lot_id = lot_no.id
                                    line.lot_name = lot_no.name
                                    line.qty_done = lot_qty



        return mo_number

