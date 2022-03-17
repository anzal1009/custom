from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from odoo import api,models, fields,_


class Purchase(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()




    # ****************************** New Purchase *****************************
    # ****************new invoice ***************





    @http.route('/create_purchase', type='json', auth='user')
    def purchase_order(self, **rec):
        # def purchase_order(self):
        if not new_invoice:
            raise UserError(_('There is an error Please check your server'))
        for row in new_invoice:
            vals = {}
            purchase_order = self.env['purchase.order'].sudo().search([('order_id', '=', row.partner_reference)],
                                                                      limit=1)
            partner_id = row.vat and self.env['res.partner'].sudo().search([('GSTIN', '=', row.vat)],
                                                                           limit=1).id or False
        if not partner_id:
            raise UserError(_('There is an error Please check your server'))
        for row in partner_id:
            vendor_details = {
                'name': row[1],
                'currency_id': 20,
                'street': row[3],
                'street2': " ",
                'city': " ",
                'zip': " ",
                'phone': " ",
                'email': " ",
                'vat': row[4],
                'parent_id': 1
            }
        partner_id = self.env['res.partner'].sudo().create({'name': 'row.Vendor_name'})
        self.env.cr.commit()

        # print(row.SALES_ORDER_NUMBER)
        # exit()

        if not purchase_order:
            order_line = []
            for row in invoice:
                invoice_date = row.TRANSACTION_DATE
                product_id = self.env['product.product'].sudo().search([('name', '=', row.ITEM_DESC)], limit=1) or False

                if not product_id:
                    uom_ids = self.env['uom.uom'].sudo().search([])
                    unit_id = self.env.ref('uom.product_uom_unit') and self.env.ref('uom.product_uom_unit').id or False
                    for record in uom_ids:
                        if record.name.upper() == row.TRANSACTION_UOM.upper():
                            unit_id = record.id
                            break

                    try:
                        product_line_dict = {

                            'name': row.ITEM_DESC,
                            'default_code': row.ITEM_NUM,
                            'list_price': row.UNIT_PRICE,
                            'l10n_in_hsn_code': row.HSN_CODE,
                            # 'uom_id': unit_id,
                            # 'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'categ_id': 1,
                            'standard_price': row.UNIT_PRICE
                        }
                    except:
                        raise UserError(
                            _('Please verify the purchase invoice ' + ' ' + row.INVOICE_NUM + ' for item ' + row.ITEM_DESC))
                    product_id = self.env['product.template'].sudo().create(product_line_dict)
                    self.env.cr.commit()

                if product_id:
                    if product_id.categ_id:
                        categ_id = product_id.categ_id
                        if categ_id.property_cost_method != 'avarage' and categ_id.property_valuation != 'real_time':
                            raise UserError(
                                _('Please Configure Product Category Values (Costing Method and Inventory Valuation'))
                    # tax_percent = str(float(row.CGST + row.SGST))
                    tax_domain = [('amount', '=', str(int(float(row.CGST + row.SGST)))),
                                  ('type_tax_use', '=', 'purchase'),
                                  ('name', '=', "GST " + str(int(float(row.CGST + row.SGST))) + "%")]
                    if self.env.company:
                        tax_domain.append(('company_id', '=', self.env.company.id))
                    tax_variant = self.env['account.tax'].search(tax_domain, limit=1)
                    if (row.CGST or row.SGST) and not tax_variant:
                        raise UserError(_('Please Configure Tax ' + str(row.CGST) + ',' + str(row.SGST)))

                    order_line.append((0, 0, {
                        'display_type': False,
                        # 'sequence': 10,
                        'product_id': product_id.id,
                        'name': product_id.name or '',
                        'date_planned': row.TRANSACTION_DATE or False,
                        'account_analytic_id': False,
                        'product_qty': row.PRIMARY_QUANTITY or 0,
                        'qty_received_manual': 0,
                        'product_uom': product_id.uom_id.id or self.env.ref('uom.product_uom_unit') and self.env.ref(
                            'uom.product_uom_unit').id or False,
                        'price_unit': row.UNIT_PRICE or 0,
                        'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))

            if partner_id:
                purchase_order_1 = False
                # try:
                purchase_order_1 = self.env['purchase.order'].create({
                    'partner_id': partner_id,
                    'partner_ref': row.order_id or '',
                    'origin': row.order_id or '',
                    'date_order': row.TRANSACTION_DATE or False,
                    'date_approve': row.TRANSACTION_DATE or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })

                self.env.cr.commit()





# **************************** Payment ********************************




@api.multi
class DistributorAccounting(models.Model):
    _name = 'distributor.acc'

    def paymentSync(self):

        if not row_customerPayments:
            raise UserError(_('There is an error Please check your server'))
        for row in row_customerPayments:
            SaleInvoice = self.env['account.move'].search([('type', '=', 'out_invoice'), ('name', '=', row[4])])
            print(SaleInvoice.id)
            if SaleInvoice:
                SaleInvoice.action_post()
                if row[7] == 'cash':
                    journal_domain = [
                        ('type', '=', 'cash'),
                        ('company_id', '=', SaleInvoice.company_id.id),
                    ]
                else:
                    journal_domain = [
                        ('type', '=', 'bank'),
                        ('company_id', '=', SaleInvoice.company_id.id),
                    ]

                default_journal_id = self.env['account.journal'].search(journal_domain, limit=1)

                val = {
                    'payment_type': 'inbound',
                    'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id or False,
                    'partner_type': 'customer',
                    'partner_id': SaleInvoice.partner_id.id or False,
                    'amount': row[9],
                    'currency_id': self.env.company and self.env.company.currency_id and self.env.company.currency_id.id,
                    'payment_date': row[6] or False,
                    'payment_difference_handling': 'open',
                    'company_id': SaleInvoice.company_id.id or False,
                    'journal_id': default_journal_id.id or False,
                    'invoice_ids': SaleInvoice and [(6, 0, SaleInvoice.ids)] or [],
                }

                payment = self.env['account.payment'].sudo().create(val)
                self.env.cr.commit()





# ************************ Warehouse_transfer ******************************