from odoo import models, fields, api, _, http
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger
from odoo.tools.safe_eval import datetime


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
                date = datetime.strptime(shdate, '%m/%d/%Y')
                if product_name:
                    product_id = product_name and request.env['product.product'].sudo().search(
                        [('name', '=', product_name)], limit=1) or False

                    if product_id:

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
                            'location_dest_id': dest_loc.id
                        })
                    else:
                        mo_number.append({
                            'status': ("Product Not Found " ,product_name),

                        })

                if modetails:
                    mo_number.append({
                        'mo_number': modetails.name,
                        'header_id': p["moc_id"]
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
                                'location_id': op_type_id.default_location_dest_id.id,
                                'location_dest_id': prod_dest.id,
                                'reference': op_type_id.name,
                                'company_id': warehouse_data.id,
                                'move_id': lot.id
                            })

            ##mo_transfer
            for masterTransferData in row["products"]:
                picking_type = request.env['stock.picking.type'].sudo().search(
                    [('name', '=', "Internal Transfers"), ('company_id', '=', warehouse_data.id)], limit=1) or False
                location_dest_id = request.env['stock.location'].sudo().search(
                    [('name', '=', "Processing Area (Blending & Packing)"), ('company_id', '=', warehouse_data.id)],
                    limit=1) or False
                location_id = request.env['stock.location'].sudo().search(
                    [('name', '=', "Raw Material Storage"), ('company_id', '=', warehouse_data.id)], limit=1) or False

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