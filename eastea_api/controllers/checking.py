from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class MoCreation(http.Controller):

    @http.route('/create_manufacturing_orders', type='json', csrf=False, auth='public')
    def create_manufacturing_orders(self, **rec):
        mo_number = []
        modetails = []
        for row in rec["data"]:
            move_raw_ids = []
            op_type = False
            warehouse = False
            warehouse_data = False
            op_type_id = False
            for op in row["operation"]:
                origin = op["source"]
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
                        [('name', '=', op_type), ('company_id', '=', warehouse_data.id)],
                        limit=1) or False
            for comp in row["rawmaterials"]:
                item_name = comp["product"]
                producing_qty = comp["qty"]
                source_loc = op_type_id.default_location_src_id
                dest_loc = op_type_id.default_location_dest_id
                prod_dest = request.env['stock.location'].sudo().search(
                    [('name', '=', "Production"), ('company_id', '=', warehouse_data.id)], limit=1) or False
                if item_name:
                    item_id = item_name and request.env['product.product'].sudo().search(
                        [('name', '=', item_name)], limit=1) or False
                move_raw_ids.append((0, 0, {
                    'product_id': item_id.id,
                    'name': "Mo Creation",
                    'product_uom_qty': producing_qty,
                    'location_id': source_loc.id,
                    'company_id': warehouse_data.id,
                    'product_uom': item_id.uom_id.id,
                    'location_dest_id': prod_dest.id
                }))
            for p in row["products"]:
                product_name = p["product"]
                quantity = p["qty"]
                shdate = p["date"]
                blendno = p["blendno"]
                lot_no = p["lot_name"]
                date = datetime.strptime(shdate, '%m/%d/%Y')
                if product_name:
                    product_id = product_name and request.env['product.product'].sudo().search(
                        [('name', '=', product_name)], limit=1) or False
                    if product_id:
                        if lot_no:
                            lot_id = request.env['stock.production.lot'].sudo().search(
                                [('company_id', '=', warehouse_data.id),
                                 ('name', '=', lot_no), ('product_id', '=', product_id.id)])
                            if lot_id:
                                producing_lot = lot_id.id
                            else:
                                lot_number = {
                                    'name': lot_no,
                                    'product_id': product_id.id,
                                    'company_id': warehouse_data.id

                                }
                                create_lot_number = request.env['stock.production.lot'].sudo().create(
                                    lot_number)
                                new_lot_id = request.env['stock.production.lot'].sudo().search(
                                    [('company_id', '=', warehouse_data.id), ('name', '=', lot_no),
                                     ('product_id', '=', product_id.id)])
                                if new_lot_id:
                                    producing_lot = new_lot_id.id

                            modetails = request.env['mrp.production'].sudo().create({
                                'product_id': product_id.id,
                                'product_qty': quantity,
                                'blend': blendno,
                                'product_uom_id': product_id.uom_id.id,
                                'date_planned_start': date,
                                'move_raw_ids': move_raw_ids,
                                'company_id': warehouse_data.id,
                                'picking_type_id': op_type_id.id,
                                'location_src_id': source_loc.id,
                                'location_dest_id': dest_loc.id,
                                'origin': origin,
                                'lot_producing_id':producing_lot
                            })

                            if modetails:
                                mo_move_line = request.env['stock.move'].sudo().create({
                                    #                                         'picking_id': lot.picking_id.id,
                                    'product_id': product_id.id,
                                    'product_uom': product_id.uom_id.id,
                                    'product_uom_qty': quantity,
                                    #                                         'lot_id': lot_no.id,
                                    'location_id': prod_dest.id,
                                    'location_dest_id': dest_loc.id,
                                    #                                         'reference': op_type_id.name,
                                    'company_id': warehouse_data.id,
                                    'production_id': modetails.id,
                                    'name': "New"
                                })
                                mo_number.append({
                                    'mo_number': modetails.name,
                                    'header_id': p["moc_id"],
                                    'status': "Success", 'message': "MO created",
                                })
                                modetails.action_confirm()
                                request.env.cr.commit()
                                if modetails.move_raw_ids:
                                    index_id = 0
                                    for lot in modetails.move_raw_ids:
                                        comp = row["rawmaterials"][index_id]
                                        index_id = int(index_id) + 1
                                        item_name = comp["product"]
                                        product = item_name and request.env['product.product'].sudo().search(
                                            [('name', '=', item_name)], limit=1) or False
                                        if product:
                                            product_lot = comp["lot"]
                                            lot_no = request.env['stock.production.lot'].sudo().search(
                                                [('company_id', '=', warehouse_data.id), ('name', '=', product_lot),
                                                 ('product_id', '=', product.id)], limit=1)
                                            if lot_no.id:
                                                lot_qty = comp["qty"]
                                            else:
                                                lot_qty = 0
                                        move_line = request.env['stock.move.line'].sudo().create({
                                            'picking_id': lot.picking_id.id,
                                            'product_id': product.id,
                                            'product_uom_id': product.uom_id.id,
                                            'qty_done': lot_qty,
                                            'lot_id': lot_no.id,
                                            'location_id': op_type_id.default_location_src_id.id,
                                            'location_dest_id': prod_dest.id,
                                            'reference': op_type_id.name,
                                            'company_id': warehouse_data.id,
                                            'move_id': lot.id
                                        })
                        else:
                            mo_number.append({
                                'mo_number': "",
                                'header_id': p["moc_id"],
                                'status': "Fail", 'message': "Check MO Product Lot no in ODOO",

                            })

                    else:
                        mo_number.append({
                            'mo_number': "",
                            'header_id': p["moc_id"],
                            'status': "Fail", 'message': "Check MO Products in ODOO",

                        })

                    ##mo_transfer
                    if modetails:
                        for masterTransferData in row["products"]:
                            picking_type = request.env['stock.picking.type'].sudo().search(
                                [('name', '=', "Internal Transfers"), ('company_id', '=', warehouse_data.id)],
                                limit=1) or False
                            location_dest_id = request.env['stock.location'].sudo().search(
                                [('name', '=', "Processing Area (Blending & Packing)"),
                                 ('company_id', '=', warehouse_data.id)],
                                limit=1) or False
                            location_id = request.env['stock.location'].sudo().search(
                                [('name', '=', "Raw Material Storage"), ('company_id', '=', warehouse_data.id)],
                                limit=1) or False

                            picking = request.env['stock.picking'].sudo().create({
                                'location_id': location_id.id,
                                'location_dest_id': location_dest_id.id,
                                # 'partner_id': self.test_partner.id,
                                'picking_type_id': picking_type.id,
                                'immediate_transfer': False,
                                'ref': "MO Transfer - " + str(modetails.name),
                                'company_id': warehouse_data.id,
                                'origin': modetails.name
                            })
                        for componentTransferData in row["rawmaterials"]:
                            product = request.env['product.product'].sudo().search(
                                [('name', '=', componentTransferData["product"])], limit=1) or False
                            lot_no = request.env['stock.production.lot'].sudo().search(
                                [('company_id', '=', warehouse_data.id), ('name', '=', componentTransferData["lot"])])
                            if product:
                                move_receipt_1 = request.env['stock.move'].sudo().create({
                                    'name': product.name,
                                    'product_id': product.id,
                                    'product_uom_qty': componentTransferData["qty"],
                                    # 'quantity_done': line["qty_done"],
                                    'product_uom': product.uom_id.id,
                                    'picking_id': picking.id,
                                    'picking_type_id': picking_type.id,
                                    'location_id': location_id.id,
                                    'location_dest_id': location_dest_id.id,
                                    'company_id': warehouse_data.id,
                                    #                         'lot_id': lot_no.id,
                                    #                         'lot_name': lot_no.name
                                })
                                request.env.cr.commit()
                                move_receipt_line = request.env['stock.move.line'].sudo().search(
                                    [('move_id', '=', move_receipt_1.id)])
                                for move_line in move_receipt_line:
                                    if move_line:
                                        move_line.unlink()
                                request.env.cr.commit()

                                move_line = request.env['stock.move.line'].sudo().create({
                                    'picking_id': picking.id,
                                    'product_id': product.id,
                                    'product_uom_id': product.uom_id.id,
                                    'qty_done': componentTransferData["qty"],
                                    'lot_id': lot_no.id,
                                    'location_id': move_receipt_1.location_id.id,
                                    'location_dest_id': move_receipt_1.location_dest_id.id,
                                    'reference': move_receipt_1.name
                                })
                            request.env.cr.commit()

        #                         move_receipt_line.lot_id = lot_no.id
        #                         move_receipt_line.lot_name = lot_no.name
        return mo_number







class WarehouseScaTransfer(http.Controller):
    @http.route('/data/SCA/create_transfers_inv', type='json', csrf=False, auth='public')
    def sca_warehouse_transfer(self, **rec):
        transfernumber = []
        for row in rec["data"]:
            picking = []
            for record in row["picking"]:
                location_code = record["location_code"]
                destination_code = record["destination_code"]
                #                 location_source = record["location_source"]
                #                 location_destination = record["location_destination"]
                reference = record["reference"]
                source = False
                #                 if record["source"]:
                #                     source = record["source"]
                company_name = "Eastea Chai Private Limited (KL)"
                company_id = request.env['res.company'].sudo().search(
                    [('name', '=', company_name)], limit=1) or False
                picking_name = "Van to Depot Transfer"

                if destination_code == "FCTRY":
                    picking_name = "Van to Depot Transfer"
                elif location_code == "FCTRY":
                    picking_name = "Depot to Van Transfer"

                if destination_code != "FCTRY" and location_code != "FCTRY":
                    picking_name = "Van to Van Transfer"

                picking_type = request.env['stock.picking.type'].sudo().search(
                    [('name', '=', picking_name), ('company_id', '=', company_id.id)], limit=1) or False
                location_id = location_code and request.env['stock.location'].sudo().search(
                    [('loc_code', '=', location_code), ('company_id', '=', company_id.id)], limit=1) or False
                location_dest_id = destination_code and request.env['stock.location'].sudo().search(
                    [('loc_code', '=', destination_code), ('company_id', '=', company_id.id)], limit=1) or False
                #                 if reference == "DAMAGED":
                #                     location_dest_id = request.env['stock.location'].sudo().search(
                #                         [('name', 'like', "Non Salable"), ('company_id', '=', company_id.id)], limit=1) or False
                #                 if reference == "EXCESS":
                #                     location_dest_id = request.env['stock.location'].sudo().search(
                #                         [('name', 'like', "Route Excess Stock"), ('company_id', '=', company_id.id)], limit=1) or False
                #                     location_id = location_code and request.env['stock.location'].sudo().search(
                #                     [('loc_code', 'like', "CustomerLocation")], limit=1) or False

                if "Route" in location_id.name and "Depot" in location_dest_id.name:
                    picking_name = "Van to Depot Transfer"
                    picking_type = request.env['stock.picking.type'].sudo().search(
                        [('name', '=', picking_name), ('company_id', '=', company_id.id)], limit=1) or False

                    if reference == "DAMAGED":
                        dest_loc_name = destination_code + " - Stocks to Repack"
                        location_dest_id = request.env['stock.location'].sudo().search(
                            [('loc_code', '=', dest_loc_name), ('company_id', '=', company_id.id)], limit=1) or False

                    if reference == "EXCESS":
                        dest_loc_name = destination_code + " - Excess Stock"
                        location_dest_id = request.env['stock.location'].sudo().search(
                            [('loc_code', '=', dest_loc_name), ('company_id', '=', company_id.id)], limit=1) or False
                        location_id = location_code and request.env['stock.location'].sudo().search(
                            [('loc_code', 'like', "CustomerLocation")], limit=1) or False

                elif "Route" in location_id.name and "Route" in location_dest_id.name:
                    picking_name = "Van to Van Transfer"
                    picking_type = request.env['stock.picking.type'].sudo().search(
                        [('name', '=', picking_name), ('company_id', '=', company_id.id)], limit=1) or False

                elif "Depot" in location_id.name and "Route" in location_dest_id.name:
                    picking_name = "Depot to Van Transfer"
                    picking_type = request.env['stock.picking.type'].sudo().search(
                        [('name', '=', picking_name), ('company_id', '=', company_id.id)], limit=1) or False

                picking = request.env['stock.picking'].sudo().create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': picking_type.id,
                    'immediate_transfer': False,
                    'ref': "SCA - " + reference + "-" + location_code,
                    'company_id': company_id.id,
                    'origin': source
                })
                move_receipt_1 = []
                for line in row["pick_lines"]:
                    product_item = line["name"]
                    print(product_item)
                    if product_item:
                        product = product_item and request.env['product.product'].sudo().search(
                            [('default_code', '=', product_item)], limit=1) or False
                        #                         if not product:
                        #                             raise ValidationError(_("Product not found"))
                        if product:
                            move_receipt_1 = request.env['stock.move'].sudo().create({
                                'name': line["name"],
                                'product_id': product.id,
                                'product_uom_qty': line["qty"],
                                # 'quantity_done': line["qty_done"],
                                'product_uom': product.uom_id.id,
                                'picking_id': picking.id,
                                'picking_type_id': picking_type.id,
                                'location_id': location_id.id,
                                'location_dest_id': location_dest_id.id,
                                'company_id': company_id.id
                            })

                for line in picking:
                    for lines in line.move_ids_without_package:
                        if lines.product_uom_qty == lines.quantity_done:

                                if reference != "EXCESS":
                                    picking.action_confirm()
                                    picking.action_assign()
                                    picking.action_set_quantities_to_reservation()

                                    for line in picking:
                                        for lines in line.move_ids_without_package:
                                            if lines.product_uom_qty == lines.quantity_done:
                                                var = True
                                                if var == True:
                                                    picking.button_validate()

                                    picking.button_validate()
                        else:
                            pass



                #
                # if picking:
                #     if picking_type.name == "Van to Van Transfer":
                #         picking.action_confirm()
                #         picking.action_assign()
                #         picking.action_set_quantities_to_reservation()
                #         picking.button_validate()
                #         transfernumber.append({
                #             'transfersNumber': picking.name
                #         })



            if picking:
                transfernumber.append({
                    'transfersNumber': picking.name
                })
        return transfernumber







class RMpurchaseDelivery(http.Controller):
    @http.route('/inv/RMpurchaseDelivery', type='json', csrf=False, auth='public')
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
                        for product_line in row["child"]:
                            product = product_line["name"] and request.env['product.product'].sudo().search(
                                [('name', '=', product_line["name"])], limit=1) or False
                            if product:
                                for line_ids in picking.move_line_ids:
                                    if product.id == line_ids.product_id.id and product_line[
                                        "description"] == line_ids.move_id.description_picking and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:
                                        # print(line_ids.lot_name)
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
                                                [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number)])
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
                                    #                                         else:
                                    #                                             ret_data.append({
                                    #                                                 'poNumber': poNumber,
                                    #                                                 'itemName': product_line["name"],
                                    #                                                 'itemDescription': product_line["description"],
                                    #                                                 'itemLOT': product_line["lot_number"],
                                    #                                                 'status': "Failed"
                                    #                                             }
                                    #                                             )

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






































# *************** RMpurchaseDelivery ******************


class RMpurchaseDelivery(http.Controller):
    @http.route('/inv/RMpurchaseDelivery', type='json', csrf=False, auth='public')
    def RMpurchaseDelivery(self, **rec):
        ret_data = []
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
                        for product_line in row["child"]:
                            product = product_line["name"] and request.env['product.product'].sudo().search(
                                [('name', '=', product_line["name"])], limit=1) or False
                            if product:
                                for line_ids in picking.move_line_ids:
                                    if product.id == line_ids.product_id.id and product_line[
                                        "description"] == line_ids.move_id.description_picking and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:
                                        # print(line_ids.lot_name)
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
                                            print('lot_no lot_no')
                                            lot_number = {
                                                'name': product_lot_number,
                                                'product_id': product.id,
                                                'company_id': warehouse_data.id
                                            }
                                            create_lot_number = request.env['stock.production.lot'].sudo().create(
                                                lot_number)
                                            lot_no = request.env['stock.production.lot'].sudo().search(
                                                [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number)])
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
                                    #                                         else:
                                    #                                             ret_data.append({
                                    #                                                 'poNumber': poNumber,
                                    #                                                 'itemName': product_line["name"],
                                    #                                                 'itemDescription': product_line["description"],
                                    #                                                 'itemLOT': product_line["lot_number"],
                                    #                                                 'status': "Failed"
                                    #                                             }
                                    #                                             )

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