from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time



class CreateSCASales(http.Controller):
    @http.route('/data/SCA/CreateSCASales2', type='json', csrf=False, auth='public')
    def CreateSCASales(self, **rec):
        so_numbers = []
        for row in rec["data"]:

            is_gst = row["child"][0]["cgst"]
            if is_gst:
                vendor_name = "Route IntraState Sales"
            is_igst = row["child"][0]["igst"]
            if is_igst:
                vendor_name = "Route InterState Sales"

            invoice_date = row["master"]["date"]
            date = datetime.strptime(invoice_date, '%d/%m/%Y')

            # vendor_ref = row["master"]["partner_id"]["ref"]
            from_company_detail = request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            if vendor_name:
                vendor = vendor_name and request.env['res.partner'].sudo().search([('name', '=', vendor_name)],
                                                                                 limit=1) or False

                if not vendor:
                    raise ValidationError(_("Customer not found"))

            jounalname = "Route Sale"
            jounal_id = jounalname and request.env['account.journal'].sudo().search(
                [('name', '=', jounalname), ('company_id', '=', from_company_detail.id)], limit=1) or False
            print(jounal_id.id)

            customer = row["master"]["partner_id"]["customer_name"]
            code = row["master"]["partner_id"]["code"]

            if code:
                analytical_id = request.env['account.analytic.account'].sudo().search(
                    [('code', 'like', code), ('company_id', '=', from_company_detail.id)], limit=1) or False
                # print(analytical_id.id)
                if not analytical_id:
                    analytical_details = {
                        'name': row["master"]["partner_id"]["customer_name"],
                        'code': row["master"]["partner_id"]["code"],
                        'company_id': from_company_detail.id,
                    }
                    analytical_id = request.env['account.analytic.account'].sudo().create(analytical_details)

                analytical_id = request.env['account.analytic.account'].sudo().search(
                    [('code', 'like', code), ('company_id', '=', from_company_detail.id)], limit=1) or False

            location_id = request.env['stock.location'].sudo().search(
                [('loc_code', 'like', code), ('company_id', '=', from_company_detail.id)], limit=1) or False
            parent_loc = "Stock"
            parent_loc_id = request.env['stock.location'].sudo().search(
                [('name', 'like', parent_loc), ('company_id', '=', from_company_detail.id)], limit=1) or False
            if not location_id:
                location_details = {
                    'name': row["master"]["partner_id"]["customer_name"],
                    'location_id': parent_loc_id.id,
                    'loc_code': row["master"]["partner_id"]["code"],
                    'company_id': from_company_detail.id,
                }
                location_id = request.env['stock.location'].sudo().create(location_details)
            location_id = request.env['stock.location'].sudo().search(
                [('loc_code', 'like', code), ('company_id', '=', from_company_detail.id)], limit=1) or False

            order_line = []
            for product_line in row["child"]:
                product_item = product_line["name"]
                gst = product_line["cgst"] + product_line["sgst"]
                igst = product_line["igst"]
                tax = False
                tax_variant = False

                if gst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', from_company_detail.id), ('amount', '=', str(gst)),
                         ('type_tax_use', '=', "sale"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', from_company_detail.id), ('amount', '=', str(igst)),
                         ('type_tax_use', '=', "sale"),
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
                        so_numbers.append({
                            'status': "Product Not Found",
                            'Product Name': product_item,
                            'orderID': row["master"]["orderID"]
                        })

                if product:
                    order_line.append((0, 0, {
                        'display_type': False,
                        # 'sequence': 10,
                        'product_id': product.id,
                        'name': product.name or '',
                        # 'date_planned': row.TRANSACTION_DATE or False,
                        # 'account_analytic_id': False,
                        'product_uom_qty': product_line["product_qty"] or 0,
                        # 'qty_received_manual': 0,
                        'discount': ((product_line["discount"]*100))/((product_line["product_qty"]*product_line["rate"])) or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["rate"] or 0,
                        'tax_id': tax,
                    }))
            if vendor:
                sale_order_1 = request.env['sale.order'].sudo().create({
                    'partner_id': vendor.id,
                    'client_order_ref': row["master"]["orderID"] or '',
                    # 'origin': row.INVOICE_NUM or '',
                    'date_order':date,
                    # 'date_planned':date,
                    'analytic_account_id':analytical_id.id,
                    'l10n_in_journal_id':jounal_id.id,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':from_company_detail.id
                })
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    sale_order_1.l10n_in_journal_id = jounal_id.id,
                    if sale_order_1.picking_ids:
                        sale_order_1.picking_ids.location_id = location_id.id

                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return so_numbers