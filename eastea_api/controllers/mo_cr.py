from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class RMpurchaseDelivery(http.Controller):
    @http.route('/inv/RMpurchaseDelivery2', type='json', csrf=False, auth='public')
    def RMpurchaseDelivery(self, **rec):
        ret_data = []
        lot_number = []
        for row in rec["data"]:
            poNumber = row["master"]["poNumber"]
            warehouse = row["master"]["company_ware_house"]["name"]
            if (warehouse == 'JOTHIPURAM'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if (warehouse == 'KAVALANGAD'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            purchase_order_1 = request.env['purchase.order'].sudo().search(
                [('company_id', '=', warehouse_data.id), ('name', '=', poNumber)])

            if purchase_order_1:
                purchase_order_1.sudo().button_approve()
                purchase_order_1.action_view_picking()
                if purchase_order_1.picking_ids:

                    for picking in purchase_order_1.picking_ids:

                        for line_ids in picking.move_line_ids:

                            for product_line in row["child"]:
                                product = product_line["name"] and request.env['product.product'].sudo().search(
                                    [('name', '=', product_line["name"])], limit=1) or False

                                if product.id == line_ids.product_id.id:
                                    if product_line["description"] == line_ids.move_id.description_picking and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:

                                        product_lot_number = product_line["lot_number"]
                                        qty_done = product_line["qty_done"]

                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number),
                                             ('product_id', '=', product.id)])

                                        if lot_no:
                                            ret_data.append({
                                                'poNumber': poNumber,
                                                'itemName': product_line["name"],
                                                'itemDescription': product_line["description"],
                                                'itemLOT': product_line["lot_number"],
                                                'status': "Failed,Lot no already exist"
                                            }
                                            )


                                        else:
                                            #                                             print('lot_no lot_no')
                                            lot_number = {
                                                'name': product_lot_number,
                                                'product_id': product.id,
                                                'company_id': warehouse_data.id
                                            }
                                            create_lot_number = request.env['stock.production.lot'].sudo().create(
                                                lot_number)
                                            lot_no = request.env['stock.production.lot'].sudo().search(
                                                [('company_id', '=', warehouse_data.id),
                                                 ('name', '=', product_lot_number)])
                                            line_ids.lot_id = lot_no.id
                                            line_ids.lot_name = lot_no.name
                                            line_ids.qty_done = qty_done

                                            request.env.cr.commit()
                                            #                                         if line_ids.qty_done == qty_done:

                                            ret_data.append({
                                                'poNumber': poNumber,
                                                'itemName': line_ids.product_id.name,
                                                'itemDescription': line_ids.move_id.description_picking,
                                                'itemLOT': lot_no.name,
                                                'status': "Success"
                                            })


                                    else:
                                        ret_data.append({
                                            'poNumber': poNumber,
                                            'itemName': product_line["name"],
                                            'itemDescription': product_line["description"],
                                            'itemLOT': product_line["lot_number"],
                                            'status': "Failed. Please verify the Product description or State of Operation in Odoo"
                                        }
                                        )

            else:
                ret_data.append({
                    'poNumber': poNumber,
                    'status': "Failed. PO Not Found"
                })
        return ret_data

#
# class RMpurchaseDelivery(http.Controller):
#     @http.route('/inv/RMpurchaseDelivery2', type='json', csrf=False, auth='public')
#     def RMpurchaseDelivery(self, **rec):
#         ret_data = []
#         lot_number = []
#         for row in rec["data"]:
#             poNumber = row["master"]["poNumber"]
#             warehouse = row["master"]["company_ware_house"]["name"]
#             if (warehouse == 'JOTHIPURAM'):
#                 warehouse_data = warehouse and request.env['res.company'].sudo().search(
#                     [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
#             if (warehouse == 'KAVALANGAD'):
#                 warehouse_data = warehouse and request.env['res.company'].sudo().search(
#                     [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
#             purchase_order_1 = request.env['purchase.order'].sudo().search(
#                 [('company_id', '=', warehouse_data.id), ('name', '=', poNumber)])
#
#             if purchase_order_1:
#                 purchase_order_1.sudo().button_approve()
#                 purchase_order_1.action_view_picking()
#                 if purchase_order_1.picking_ids:
#                     for picking in purchase_order_1.picking_ids:
#                         for product_line in row["child"]:
#                             product = product_line["name"] and request.env['product.product'].sudo().search(
#                                 [('name', '=', product_line["name"])], limit=1) or False
#                         if product:
#                             for line_ids in picking.move_line_ids:
#                                 if product.id == line_ids.product_id.id and product_line[
#                                     "description"] == line_ids.move_id.description_picking and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:
#                                     # print(line_ids.lot_name)
#                                     product_lot_number = product_line["lot_number"]
#                                     qty_done = product_line["qty_done"]
#
#                                     lot_no = request.env['stock.production.lot'].sudo().search(
#                                         [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number),
#                                          ('product_id', '=', product.id)])
#
#                                     if lot_no:
#                                         ret_data.append({
#                                             'poNumber': poNumber,
#                                             'itemName': product_line["name"],
#                                             'itemDescription': product_line["description"],
#                                             'itemLOT': product_line["lot_number"],
#                                             'status': "Failed,Lot no already exist"
#                                         }
#                                         )
#
#
#                                     else:
# #                                             print('lot_no lot_no')
#                                         lot_number = {
#                                             'name': product_lot_number,
#                                             'product_id': product.id,
#                                             'company_id': warehouse_data.id
#                                         }
#                                         create_lot_number = request.env['stock.production.lot'].sudo().create(
#                                             lot_number)
#                                         lot_no = request.env['stock.production.lot'].sudo().search(
#                                             [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number)])
#                                         line_ids.lot_id = lot_no.id
#                                         line_ids.lot_name = lot_no.name
#                                         line_ids.qty_done = qty_done
#
#                                         request.env.cr.commit()
#                                     #                                         if line_ids.qty_done == qty_done:
#
#                                         ret_data.append({
#                                             'poNumber': poNumber,
#                                             'itemName': line_ids.product_id.name,
#                                             'itemDescription': line_ids.move_id.description_picking,
#                                             'itemLOT': lot_no.name,
#                                             'status': "Success"
#                                         })
#                                 #                                         else:
#                                 #                                             ret_data.append({
#                                 #                                                 'poNumber': poNumber,
#                                 #                                                 'itemName': product_line["name"],
#                                 #                                                 'itemDescription': product_line["description"],
#                                 #                                                 'itemLOT': product_line["lot_number"],
#                                 #                                                 'status': "Failed"
#                                 #                                             }
#                                 #                                             )
#
#                                 else:
#                                     ret_data.append({
#                                         'poNumber': poNumber,
#                                         'itemName': product_line["name"],
#                                         'itemDescription': product_line["description"],
#                                         'itemLOT': product_line["lot_number"],
#                                         'status': "Failed. Please verify the Product description or State of Operation in Odoo"
#                                     }
#                                     )
#
#             else:
#                 ret_data.append({
#                     'poNumber': poNumber,
#                     'status': "Failed. PO Not Found"
#                 })
#         return ret_data
