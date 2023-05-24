from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class TaxConvertion(http.Controller):

    @http.route('/tax_convertion', type='json', csrf=False, auth='public')
    def tax_convertion(self, **rec):

        gst = request.env['account.tax'].sudo().search(
            [('name', '=', "GST 5%"),('type_tax_use', '=', "purchase")], limit=1)

        purchase_order= request.env['purchase.order'].sudo().search([]) or False
        for po in purchase_order:
            for line in po.order_line:
                line.taxes_id = gst




class MoveToDraft(http.Controller):
    @http.route('/reset_to_draft', type='json', csrf=False, auth='public')
    def tax_convertion(self, **rec):

        po_bill =request.env['account.move'].sudo().search([('move_type','=','in_invoice'),('state','=','posted')]) or False

        for bill in po_bill:
            bill.button_draft()






class RMpurchaseDelivery(http.Controller):
    @http.route('/inv/RMpurchaseDelivery', type='json', csrf=False, auth='public')
    def RMpurchaseDelivery(self, **rec):
        ret_data = []
        for row in rec["data"]:
            poNumber = row["master"]["poNumber"]
            warehouse = row["master"]["company_ware_house"]["name"]
            if (warehouse == 'JOTHIPURAM'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                [('name', '=', 'Eastea Chai Private Limited (TN)')], limit=1) or False
            if (warehouse == 'KAVALANGAD'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            purchase_order_1 = request.env['purchase.order'].sudo().search(
                [('company_id', '=', warehouse_data.id), ('name', '=', poNumber)])

            if purchase_order_1:
                if purchase_order_1.state != "purchased":
                    purchase_order_1.button_confirm()
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            for product_line in row["child"]:
                                product = product_line["name"] and request.env['product.product'].sudo().search(
                                    [('name', '=', product_line["name"])], limit=1) or False
                                print(product.name)
                                if product:
                                    for line_ids in picking.move_line_ids:
                                        if product.id == line_ids.product_id.id:
                                            if product.name == product_line["description"]:
                                                if line_ids.move_id.state == "assigned":
                                                    if line_ids.lot_name == False:

                                                        product_lot_number = product_line["lot_number"]
                                                        qty_done = product_line["qty_done"]
                                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                                            [('company_id', '=', warehouse_data.id),
                                                             ('name', '=', product_lot_number),
                                                             ('product_id', '=', product.id)])
                                                        if not lot_no:
                                                            print('lot_no lot_no')
                                                            lot_number = {
                                                                'name': product_lot_number,
                                                                'product_id': product.id,
                                                                'company_id': warehouse_data.id
                                                            }
                                                            create_lot_number = request.env[
                                                                'stock.production.lot'].sudo().create(lot_number)
                                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                                            [('company_id', '=', warehouse_data.id),
                                                             ('name', '=', product_lot_number)])
                                                        line_ids.lot_id = lot_no.id
                                                        line_ids.lot_name = lot_no.name
                                                        line_ids.qty_done = qty_done

                                                        if line_ids.qty_done == qty_done:
                                                            ret_data.append({
                                                                'poNumber': poNumber,
                                                                'itemName': line_ids.product_id.name,
                                                                'itemDescription': line_ids.move_id.name,
                                                                'itemLOT': lot_no.name,
                                                                'status': "Success"
                                                            })
                                                        else:
                                                            ret_data.append({
                                                                'poNumber': poNumber,
                                                                'itemName': product_line["name"],
                                                                'itemDescription': product_line["description"],
                                                                'itemLOT': product_line["lot_number"],
                                                                'status': "Failed"
                                                            })
                                                    else:
                                                        ret_data.append({
                                                            'poNumber': poNumber,
                                                            'itemName': product_line["name"],
                                                            'itemDescription': product_line["description"],
                                                            'itemLOT': product_line["lot_number"],
                                                            'status': "Failed.Transfer Validation Pending"
                                                        })
                                                # else:
                                                #     ret_data.append({
                                                #         'poNumber': poNumber,
                                                #         'itemName': product_line["name"],
                                                #         'itemDescription': product_line["description"],
                                                #         'itemLOT': product_line["lot_number"],
                                                #         'status': "Failed.LOT no Already Existing "
                                                #     })
                                            else:
                                                ret_data.append({
                                                    'poNumber': poNumber,
                                                    'itemName': product_line["name"],
                                                    'itemDescription': product_line["description"],
                                                    'itemLOT': product_line["lot_number"],
                                                    'status': "Failed.Please Check the Product Discription And try Again"
                                                })
                                                
                                        # else:
                                        #     ret_data.append({
                                        #         'poNumber': poNumber,
                                        #         'itemName': product_line["name"],
                                        #         'itemDescription': product_line["description"],
                                        #         'itemLOT': product_line["lot_number"],
                                        #         'status': "Failed.Product Doesnot Exist"
                                        #     })

            else:
                ret_data.append({
                    'poNumber': poNumber,
                    'status': "Failed. PO Not Found"
                })
        return ret_data
















                                        # if product.id == line_ids.product_id.id and product_line["description"] ==  line_ids.move_id.name and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:
                                        #     # print(line_ids.lot_name)
                                        #     product_lot_number = product_line["lot_number"]
                                        #     qty_done = product_line["qty_done"]
                                        #     lot_no = request.env['stock.production.lot'].sudo().search(
                                        #         [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number),('product_id', '=', product_line["name"])])
                                        #     if not lot_no:
                                        #         print('lot_no lot_no')
                                        #         lot_number = {
                                        #             'name': product_lot_number,
                                        #             'product_id': product.id,
                                        #             'company_id': warehouse_data.id
                                        #         }
                                        #         create_lot_number = request.env['stock.production.lot'].sudo().create(lot_number)
                                        #     lot_no = request.env['stock.production.lot'].sudo().search(
                                        #         [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number)])
                                        #     line_ids.lot_id = lot_no.id
                                        #     line_ids.lot_name = lot_no.name
                                        #     line_ids.qty_done = qty_done
        #                                     if line_ids.qty_done == qty_done:
        #                                         ret_data.append({
        #                                             'poNumber': poNumber,
        #                                             'itemName': line_ids.product_id.name,
        #                                             'itemDescription': line_ids.move_id.name,
        #                                             'itemLOT': lot_no.name,
        #                                             'status': "Success"
        #                                         })
        #                                     else:
        #                                         ret_data.append({
        #                                             'poNumber': poNumber,
        #                                             'itemName': product_line["name"],
        #                                             'itemDescription': product_line["description"],
        #                                             'itemLOT': product_line["lot_number"],
        #                                             'status': "Failed"
        #                                         }
        #                                         )
        #
        #                                 elif product.id == line_ids.product_id.id and product_line["description"] == line_ids.move_id.name and line_ids.move_id.state == "assigned" and line_ids.lot_name != False:
        #                                     ret_data.append({
        #                                         'poNumber': poNumber,
        #                                         'itemName': product_line["name"],
        #                                         'itemDescription': product_line["description"],
        #                                         'itemLOT': product_line["lot_number"],
        #                                         'status': "Failed"
        #                                     }
        #                                     )
        #
        #     else:
        #         ret_data.append({
        #             'poNumber': poNumber,
        #             'status': "Failed. PO Not Found"
        #         })
        # return ret_data
        #
