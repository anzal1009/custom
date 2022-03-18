from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from odoo import api, models, fields, _


#
# class MyController(odoo.http.Controller):
#     @route('/some_url', auth='public')
#     def handler(self):
#         print("boom")
#         return stuff()


class Purchase(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    # ****************************** New Purchase *****************************
    # ****************new invoice ***************

    @http.route('/data/create_rm_purchase', type='json', auth='user')
    def create_rm_purchase(self, **rec):
        for row in rec["data"]:
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
                            'list_price': product_line["price_unit"],
                            # 'l10n_in_hsn_code': row.HSN_CODE,
                            'uom_id': unit_id,
                            'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'categ_id': 1,
                            'standard_price': product_line["price_unit"],

                        }

                        product = request.env['product.template'].sudo().create(product_details)
                        request.env.cr.commit()
                    order_line = []
                    if product:
                        order_line.append((0, 0, {
                            'display_type': False,
                            # 'sequence': 10,
                            'product_id': product.id,
                            'name': product.name or '',
                            # 'date_planned': row.TRANSACTION_DATE or False,
                            'account_analytic_id': False,
                            'product_qty': product_line["product_qty"] or 0,
                            'qty_received_manual': 0,
                            # 'discount': discount or 0,
                            'product_uom': product.uom_id.id or request.env.ref(
                                'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                            'price_unit': product_line["price_unit"] or 0,
                            # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                        }))




            if vendor:
                purchase_order_1 = request.env['purchase.order'].create({
                    'partner_id': vendor.id ,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    # 'date_order':row["master"]["date_order"] or False,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })

                request.env.cr.commit()

        


# **************************** Payment ********************************

#
# @api.multi
# class DistributorAccounting(models.Model):
#     _name = 'distributor.acc'
#
#     def paymentSync(self):
#
#         if not row_customerPayments:
#             raise UserError(_('There is an error Please check your server'))
#         for row in row_customerPayments:
#             SaleInvoice = self.env['account.move'].search([('type', '=', 'out_invoice'), ('name', '=', row[4])])
#             print(SaleInvoice.id)
#             if SaleInvoice:
#                 SaleInvoice.action_post()
#                 if row[7] == 'cash':
#                     journal_domain = [
#                         ('type', '=', 'cash'),
#                         ('company_id', '=', SaleInvoice.company_id.id),
#                     ]
#                 else:
#                     journal_domain = [
#                         ('type', '=', 'bank'),
#                         ('company_id', '=', SaleInvoice.company_id.id),
#                     ]
#
#                 default_journal_id = self.env['account.journal'].search(journal_domain, limit=1)
#
#                 val = {
#                     'payment_type': 'inbound',
#                     'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id or False,
#                     'partner_type': 'customer',
#                     'partner_id': SaleInvoice.partner_id.id or False,
#                     'amount': row[9],
#                     'currency_id': self.env.company and self.env.company.currency_id and self.env.company.currency_id.id,
#                     'payment_date': row[6] or False,
#                     'payment_difference_handling': 'open',
#                     'company_id': SaleInvoice.company_id.id or False,
#                     'journal_id': default_journal_id.id or False,
#                     'invoice_ids': SaleInvoice and [(6, 0, SaleInvoice.ids)] or [],
#                 }
#
#                 payment = self.env['account.payment'].sudo().create(val)
#                 self.env.cr.commit()
#
#

# ************************ Warehouse_transfer ******************************

    @http.route('/get_products', type='json', auth='user')
    def get_products(self):
        print("Yes here entered")
        patients_rec = request.env['product.template'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                'name': rec.name,
                'qty': rec.qty_available,
                'loc': rec.property_stock_inventory.name,
                'id': rec.company_id,
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data
