from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class SalesDelivery(http.Controller):
    @http.route('/inv/SalesDelivery', type='json', csrf=False, auth='public')
    def SalesDelivery(self, **rec):
        ret_data = []
        for row in rec["data"]:
            soNumber = row["master"]["soNumber"]
            warehouse = row["master"]["company_ware_house"]["name"]
            if (warehouse == 'JOTHIPURAM'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (TN)')], limit=1) or False
            if (warehouse == 'KAVALANGAD'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            sale_order_1 = request.env['sale.order'].sudo().search(
                [('company_id', '=', warehouse_data.id), ('name', '=', soNumber)])
            print(sale_order_1)

            if sale_order_1:
                if sale_order_1.state != "sale":
                    sale_order_1.action_confirm()
                if sale_order_1.picking_ids:
                    for picking in sale_order_1.picking_ids:
                        for product_line in row["child"]:
                            product = product_line["name"] and request.env['product.product'].sudo().search(
                                [('name', '=', product_line["name"])], limit=1) or False
                            if product:
                                for line_ids in picking.move_line_ids:
                                    if product.id == line_ids.product_id.id and product_line[
                                        "description"] == line_ids.move_id.name and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:
                                        # print(line_ids.lot_name)
                                        product_lot_number = product_line["lot_number"]
                                        qty_done = product_line["qty_done"]
                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', warehouse_data.id),
                                             ('name', '=', product_lot_number),
                                             ('product_id', '=', product_line["name"])])
                                        print(lot_no)
                                        if not lot_no:
                                            raise ValidationError(_("Lot Number not exist"))
                                            # ret_data.append({
                                            #     'soNumber': soNumber,
                                            #     'itemName': product_line["name"],
                                            #     'itemDescription': product_line["description"],
                                            #     'status': "Failed.Lot No Not Found"
                                            # })

                                        #     print('lot_no lot_no')
                                        #     lot_number = {
                                        #         'name': product_lot_number,
                                        #         'product_id': product.id,
                                        #         'company_id': warehouse_data.id
                                        #     }
                                        #     create_lot_number = request.env['stock.production.lot'].sudo().create(
                                        #         lot_number)
                                        # lot_no = request.env['stock.production.lot'].sudo().search(
                                        #     [('company_id', '=', warehouse_data.id),
                                        #      ('name', '=', product_lot_number)])
                                        line_ids.lot_id = lot_no.id
                                        line_ids.lot_name = lot_no.name
                                        line_ids.qty_done = qty_done
                                        if line_ids.qty_done == qty_done:
                                            ret_data.append({
                                                'poNumber': soNumber,
                                                'itemName': line_ids.product_id.name,
                                                'itemDescription': line_ids.move_id.name,
                                                'itemLOT': lot_no.name,
                                                'status': "Success"
                                            })
                                        else:
                                            ret_data.append({
                                                'soNumber': soNumber,
                                                'itemName': product_line["name"],
                                                'itemDescription': product_line["description"],
                                                'itemLOT': product_line["lot_number"],
                                                'status': "Failed"
                                            }
                                            )

                                    elif product.id == line_ids.product_id.id and product_line[
                                        "description"] == line_ids.move_id.name and line_ids.move_id.state == "assigned" and line_ids.lot_name != False:
                                        ret_data.append({
                                            'soNumber': soNumber,
                                            'itemName': product_line["name"],
                                            'itemDescription': product_line["description"],
                                            'itemLOT': product_line["lot_number"],
                                            'status': "Failed. Please verify the Transaction in Odoo"
                                        }
                                        )

            else:
                ret_data.append({
                    'soNumber': soNumber,
                    'status': "Failed. SO Not Found"
                })
        return ret_data
