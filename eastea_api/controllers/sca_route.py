from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time


class WarehouseScaTransfer(http.Controller):
    @http.route('/data/SCA/create_transfers_inv1', type='json', csrf=False, auth='public')
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
                company_name = "Eastea Chai Private Limited (KL)"

                company_id = request.env['res.company'].sudo().search(
                    [('name', '=', company_name)], limit=1) or False

                picking_type = request.env['stock.picking.type'].sudo().search(
                    [('name', '=', 'Internal Transfers'), ('company_id', '=', company_id.id)], limit=1) or False

                location_id = location_code and request.env['stock.location'].sudo().search(
                    [('loc_code', '=', location_code), ('company_id', '=', company_id.id)], limit=1) or False

                location_dest_id = destination_code and request.env['stock.location'].sudo().search(
                    [('loc_code', '=', destination_code), ('company_id', '=', company_id.id)], limit=1) or False

                if reference == "DAMAGED":
                    location_dest_id = request.env['stock.location'].sudo().search(
                        [('name', 'like', "Non Salable"), ('company_id', '=', company_id.id)], limit=1) or False

                picking = request.env['stock.picking'].sudo().create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': picking_type.id,
                    'immediate_transfer': False,
                    'ref': " SCA " + reference,
                    'company_id': company_id.id
                })
                move_receipt_1 = []
                for line in row["pick_lines"]:
                    product_item = line["name"]
                    print(product_item)
                    if product_item:
                        product = product_item and request.env['product.product'].sudo().search(
                            [('default_code', '=', product_item)], limit=1) or False
                        if not product:
                            raise ValidationError(_("Product not found"))

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

            if picking:
                transfernumber.append({
                    'transfersNumber': picking.name
                })
        return transfernumber
