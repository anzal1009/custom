from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _



class CustomerPayment(http.Controller):

    @http.route('/create_customer_payments', type='json', auth='user')
    def create_customer_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                customer_name = record["name"]
                print(customer_name)

                testeddate = record['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')
                print(date)

                if customer_name:
                    customer_id = customer_name and request.env['res.partner'].sudo().search(
                        [('name', '=', customer_name)], limit=1) or False
                    print(customer_id.id)

            payment_details = []
            payment_details = request.env['account.payment'].create({
                'partner_id': customer_id.id,
                'amount': record["amount"],
                'date': date,
                # 'ref': record["refe"],
                'payment_type':record["payment_type"],
                'bank_reference':record["bank"],
                'cheque_reference':record["cheque"],
                'pay_ref':record["payment_reference"]

            })
            if payment_details:
                paymnt_number.append({
                    'paymntNumber': payment_details.id
                })
            return paymnt_number


# **********************Warehouse Transfer********************

class WareHouseTransfer(http.Controller):

    @http.route('/create_transfers', type='json', auth='user')
    def action_approve(self, **rec):

        trnsNmbr = []
        if request.jsonrequest:

            picking_type = request.env['stock.picking.type'].sudo().search(
                [('name', '=', 'Internal Transfers')], limit=1) or False
            picking = []

            for record in rec["picking"]:
                location_source = record["location_source"]
                location_destination = record["location_destination"]

                if location_source:
                    location_id = location_source and request.env['stock.location'].sudo().search(
                        [('name', '=', location_source)], limit=1) or False
                    location_dest_id = location_destination and request.env['stock.location'].sudo().search(
                        [('name', '=', location_destination)], limit=1) or False

                picking = request.env['stock.picking'].create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': picking_type.id,
                    'immediate_transfer': False,
                })
            move_receipt_1 = []
            for line in rec["pick_lines"]:
                location_name = location_id
                location_dest_id = location_dest_id
                product_item = line["name"]

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
                        raise ValidationError(_("Product not found"))

                move_receipt_1 = request.env['stock.move'].create({
                    'name': line["name"],
                    'product_id': product.id,
                    'product_uom_qty': line["qty"],
                    # 'quantity_done': line["qty_done"],
                    'product_uom': 12,
                    'picking_id': picking.id,
                    'picking_type_id': picking_type.id,
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                })

        if picking:
            trnsNmbr.append({
                'TrnsfrNumber': picking.name
            })
        return trnsNmbr


# ************************Sales Order****************************

class ScaSalesOrder(http.Controller):

    @http.route('/data/create_scm_sales', type='json', auth='user')
    def create_rm_sales(self, **rec):
        so_numbers = []
        for row in rec["data"]:

            invoice_date = row["master"]["date"]
            print(invoice_date)
            date = datetime.strptime(invoice_date, '%d/%m/%Y')
            print(date)

            vendor_gst = row["master"]["partner_id"]["gst_no"]
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
                            'categ_id': 1,
                            'standard_price': product_line["rate"],
                        }
                        product = request.env['product.template'].sudo().create(product_details)
                        request.env.cr.commit()
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
                        # 'discount': discount or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["rate"] or 0,
                        # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))
            if vendor:
                sale_order_1 = request.env['sale.order'].create({
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    'date_order':date,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
            return so_numbers



#*************************** Credit Note ******************


















