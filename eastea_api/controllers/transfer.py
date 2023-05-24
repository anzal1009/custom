from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _






class RawMaterialInternalTransfer(http.Controller):
    @http.route('/data/RawMaterialInternalTransfer', type='json', csrf=False, auth='public')
    def RawMaterialInternalTransfer(self, **rec):


        so_numbers = []
        for row in rec["data"]:

            invoice_date = row["master"]["date"]
            date = datetime.strptime(invoice_date, '%d/%m/%Y')

            vendor_gst = row["master"]["partner_id"]["gst_no"]
            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'JOTHIPURAM'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if (sale_to_company == 'KAVALANGAD'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

            sale_from_company = row["master"]["partner_id"]["name"]
            if (sale_from_company == 'JOTHIPURAM'):
                from_company_detail = sale_from_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if (sale_from_company == 'KAVALANGAD'):
                from_company_detail = sale_from_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            if vendor_gst:
                vendor = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
                                                                                 limit=1) or False
#                 if not vendor:
#                     vendor_details = {
#                         'name': row["master"]["partner_id"]["name"],
#                         'company_type': "company",
#                         'currency_id': 20,
#                         'street': row["master"]["partner_id"]["address"],
#                         'l10n_in_gst_treatment': "regular",
#                         'street2': " ",
#                         'city': " ",
#                         'zip': " ",
#                         'phone': row["master"]["partner_id"]["phone"],
#                         'email': row["master"]["partner_id"]["email"],
#                         'vat': row["master"]["partner_id"]["gst_no"],
#                         # 'parent_id': 1
#                     }
#                     vendor = request.env['res.partner'].sudo().create(vendor_details)
#                     request.env.cr.commit()
            order_line = []
            for product_line in row["child"]:
                product_item = product_line["name"]
                gst = product_line["cgst"] + product_line["sgst"]
                igst = product_line["igst"]
                if gst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', from_company_detail.id), ('amount', '=', str(gst)), ('type_tax_use', '=',"sale"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', from_company_detail.id), ('amount', '=', str(igst)), ('type_tax_use', '=',"sale"),
                         ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)

                tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False

                if product_item:
                    product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    uom_ids = request.env['uom.uom'].sudo().search([])
                    unit_id = request.env.ref('uom.product_uom_unit') and request.env.ref(
                        'uom.product_uom_unit').id or False
                    for record in uom_ids:
                        if record.name == "kg":
                            unit_id = record.id
                    if not product:
                        product_details = {
                            'name': product_line["name"],
                            # 'default_code': row.ITEM_NUM,
                            'list_price': product_line["rate"],
                            # 'l10n_in_hsn_code': row.HSN_CODE,
                            'uom_id': unit_id,
                            'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'tracking':'lot',
                            'categ_id': 1,
                            'standard_price': product_line["rate"],
                        }
                        add_product = request.env['product.template'].sudo().create(product_details)
                        request.env.cr.commit()
                        product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    if product:
                        product_lot_number = product_line["lot_number"]
                        qty_done = product_line["qty_done"]
                        lot_no = request.env['stock.production.lot'].sudo().search(
                            [('company_id', '=', from_company_detail.id), ('name', '=', product_lot_number)])
                        order_line.append((0, 0, {
                            'display_type': False,
                            # 'sequence': 10,
                            'product_id': product.id,
                            'name': product_line["description"] or '',
                            # 'date_planned': row.TRANSACTION_DATE or False,
                            # 'account_analytic_id': False,
                            'product_uom_qty': product_line["product_qty"] or 0,
                            # 'qty_received_manual': 0,
                            # 'discount': discount or 0,
                            'product_uom': product.uom_id.id or request.env.ref(
                                'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                            'price_unit': product_line["rate"] or 0,
                            'tax_id': tax,
                        }))
            if to_company_detail2:
                sale_order_1 = request.env['sale.order'].sudo().create({
                    'partner_id': to_company_detail2.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    'date_order':date,
                    'date_planned':date,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':from_company_detail.id
                })
#                 request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    if sale_order_1.picking_ids:
                        for picking in sale_order_1.picking_ids:
                            for product_line in row["child"]:
                                product_lot_number = product_line["lot_number"]
                                product = product_line["name"] and request.env['product.product'].sudo().search(
                                    [('name', '=', product_line["name"])], limit=1) or False
                                if product:
                                    for line_ids in picking.move_line_ids:
                                        if product.id == picking.product_id.id and product_line[
                                            "description"] == line_ids.move_id.name:
                                            product_lot_number = product_line["lot_number"]
                                            qty_done = product_line["qty_done"]
                                            lot_no = request.env['stock.production.lot'].sudo().search(
                                                [('company_id', '=', from_company_detail.id),
                                                 ('name', '=', product_lot_number)])
                                            line_ids.lot_id = lot_no.id
                                            line_ids.lot_name = lot_no.name
                                            line_ids.qty_done = qty_done
#                             picking.button_validate()
#                             pick_to_backorder = request.env['stock.immediate.transfer']
#                             stock_immediate = pick_to_backorder.sudo().create(
#                                 {'pick_ids': [(6, 0, sale_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                so_numbers.append({
                    'soNumber': sale_order_1.name,
                    'orderID': row["master"]["orderID"]
                })
        po_numbers = []
        for row in rec["data"]:
            vendor_gst = row["master"]["partner_id"]["gst_no"]
            purchase_to_company = row["master"]["company_ware_house"]["name"]
            if purchase_to_company == 'JOTHIPURAM':
                purchase_to_company_detail2 = purchase_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if purchase_to_company == 'KAVALANGAD':
                purchase_to_company_detail2 = purchase_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

            purchase_from_company = row["master"]["partner_id"]["name"]
            if purchase_from_company == 'JOTHIPURAM':
                purchase_from_company_detail = purchase_from_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if purchase_from_company == 'KAVALANGAD':
                purchase_from_company_detail = purchase_from_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            if vendor_gst:
                vendor = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
                                                                                 limit=1) or False
                if not vendor:
                    vendor_details = {
                        'name': row["master"]["partner_id"]["name"],
                        'company_type': "company",
                        'currency_id': 20,
                        'street': row["master"]["partner_id"]["address"],
                        'l10n_in_gst_treatment': "regular",
                        'street2': " ",
                        'city': " ",
                        'zip': " ",
                        'phone': row["master"]["partner_id"]["phone"],
                        'email': row["master"]["partner_id"]["email"],
                        'vat': row["master"]["partner_id"]["gst_no"],
                        # 'parent_id': 1
                    }
                    vendor = request.env['res.partner'].sudo().create(vendor_details)
                    request.env.cr.commit()
            order_line = []
            for product_line in row["child"]:
                product_item = product_line["name"]
                gst = product_line["cgst"] + product_line["sgst"]
                igst = product_line["igst"]
                if gst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', purchase_to_company_detail2.id), ('amount', '=', str(gst)), ('type_tax_use', '=', "purchase"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', purchase_to_company_detail2.id), ('amount', '=', str(igst)), ('type_tax_use', '=', "purchase"),
                         ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)

                tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                if product_item:
                    product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    uom_ids = request.env['uom.uom'].sudo().search([])
                    unit_id = request.env.ref('uom.product_uom_unit') and request.env.ref(
                        'uom.product_uom_unit').id or False
                    for record in uom_ids:
                        if record.name == "kg":
                            unit_id = record.id
                    if not product:
                        product_details = {
                            'name': product_line["name"],
                            # 'default_code': row.ITEM_NUM,
                            'list_price': product_line["rate"],
                            # 'l10n_in_hsn_code': row.HSN_CODE,
                            'uom_id': unit_id,
                            'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'tracking':'lot',
                            'categ_id': 1,
                            'standard_price': product_line["rate"],

                        }

                        add_product = request.env['product.template'].sudo().create(product_details)
                        request.env.cr.commit()
                        product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    if product:
                        order_line.append((0, 0, {
                            'display_type': False,
                            # 'sequence': 10,
                            'product_id': product.id,
                            'name': product_line["description"] or '',
                            # 'date_planned': row.TRANSACTION_DATE or False,
                            'account_analytic_id': False,
                            'product_qty': product_line["product_qty"] or 0,
                            'qty_received_manual': 0,
                            # 'discount': discount or 0,
                            'product_uom': product.uom_id.id or request.env.ref(
                                'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                            'price_unit': product_line["rate"] or 0,
                            'taxes_id': tax,
                        }))
            if vendor:
                purchase_order_1 = request.env['purchase.order'].sudo().create({
                    'partner_id': purchase_from_company_detail.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    'date_order':date,
                    'date_planned':date,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':purchase_to_company_detail2.id
                })
#                 request.env.cr.commit()

                if purchase_order_1:
                    purchase_order_1.button_confirm()
                    purchase_order_1.button_approve()
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return po_numbers, so_numbers