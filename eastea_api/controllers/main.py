from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from odoo import api, models, fields, _


class Purchase(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    # ****************************** New Purchase *****************************
    # ****************new invoice ***************

    @http.route('/data/create_rm_purchase', type='json', auth='user')
    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
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
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    # 'date_order':row["master"]["date_order"] or False,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()

                if purchase_order_1:
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return po_numbers

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

    # **************stock_details***********

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
                'uom': rec.product_id.uom_id
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data

    # ****************Inventory_Transfer_details**********

    @http.route('/get_transfer', type='json', auth='user')
    def get_transfers(self):

        print("Yes here entered")
        patients_rec = request.env['stock.move'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                # 'name': rec.location_id,
                'opera': rec.picking_type_id.name,
                'dest': rec.location_dest_id.name,
                'loca': rec.location_id.name,
                'name': rec.product_id.name,
                'product_id': rec.product_id,
                'qty': rec.product_uom_qty,
                'uom': rec.product_id.uom_id.name,
                # 'name': rec.product_id.name,
                # 'res':rec.reserved_availability,
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data

    @http.route('/create_transfers', type='json', auth='user')
    def create_customer(self, **rec):
        if request.jsonrequest:
            print("rec", rec)
            if rec['operation']:
                vals = {
                    'picking_type_id': rec["operation"],
                    'location_dest_id': rec['destination'],
                    'location_id': rec['location'],
                    'description_picking': rec['des'],
                    'product_id': rec['product_id'],
                    'product_uom_qty': rec['qty'],
                    'product_uom': rec['uom'],
                    'name': rec['name']
                }
                new_customer = request.env['stock.move'].sudo().create(vals)
                print("New Customer Is", new_customer)
                args = {'success': True, 'message': 'Success', 'id': new_customer.id}
        return args

    @http.route('/create_transfers_inv', type='json', auth='user')
    def action_approve(self, **rec):
        if request.jsonrequest:
            picking = []

            for record in rec["picking"]:
                picking = request.env['stock.picking'].create({
                    'location_id': record["location"],
                    'location_dest_id': record["location_dest"],
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': 19,
                    'immediate_transfer': False,
                })
                location_id = record["location"]
                print(location_id)
                location_dest_id =record["location_dest"]
                print(location_dest_id)
            move_receipt_1 = []

            for line in rec["pick_lines"]:
                #
                # print(line["name"])
                # print( record["location_dest"])
                location_id = record["location"]


                move_receipt_1 = request.env['stock.move'].create({
                    'name': line["name"],
                    'product_id': 41,
                    'product_uom_qty': line["qty"],
                    'quantity_done': line["qty_done"],
                    'product_uom': 1,
                    'picking_id': picking.id,
                    'picking_type_id': 19,
                    'location_id': record["location"],
                    'location_dest_id':location_dest_id,
                })
        # if move_receipt_1:
        #
        #     record.state = 'approved'
        #     record.approved_date = fields.Datetime.now()
        #     record.approved_by = request.env.uid
        # else:
        #     raise ValidationError(_("Something went wrong during your Request generation"))
        # return True

        # if request.jsonrequest:
        #     print("rec", rec)
        #
        # for record in rec:
        #     pick_lines = []
        #     for line in rec["pick_lines"]:
        #         pick_line_values = {
        #             # 'product_id.name': line['name'],
        #             'product_id': line['product_id'],
        #             'product_uom_qty': line['qty'],
        #             'product_uom': line['uom'],
        #             # 'name': line['des'],
        #             'state': 'draft',
        #             'name':'eee',
        #             'location_id': 29,
        #             'location_dest_id': 8,
        #             'picking_type_id': 19,
        #         }
        #         pick_lines.append((0, 0, pick_line_values))
        #         print(pick_lines)
        # picking = {
        #     'location_id': "29",
        #     'location_dest_id': "8",
        #     'move_type': 'direct',
        #     'picking_type_id': 19,
        #     # 'ctsrf': record.id,
        #     'move_lines': pick_lines,
        # }
        # print(picking)

        # picking = request.env['stock.picking'].sudo().create({
        #
        #     'location_id': 29,
        #     'location_dest_id': 8,
        #     # 'partner_id': self.test_partner.id,
        #     'picking_type_id': 19,
        #     'immediate_transfer': False,

        # })

        # move_receipt_1 = request.env['stock.move'].create({
        #     # 'name': self.kit_parent.name,
        #     'product_id': "41",
        #     'product_uom_qty': 3,
        #     'product_uom': "Units",
        #     'picking_id': picking.id,
        #     'picking_type_id': 19,
        #     'location_id': 29,
        #     'location_dest_id': 8,
        # })
        # picking.action_confirm()

        #     'location_id': "29",
        #     'location_dest_id': "8",
        #     # 'partner_id': self.test_partner.id,
        #     'picking_type_id': "19",
        #     'immediate_transfer': False,
        # })

        # transfer = request.env['stock.picking'].sudo().create(picking)

        #     if transfer:
        #         record.state = 'approved'
        #         record.approved_date = fields.Datetime.now()
        #         record.approved_by = self.env.uid
        #     else:
        #         raise ValidationError(_("Something went wrong during your Request generation"))
        # return True
        #

    # ******************Sales Orders********************

    @http.route('/get_sales', type='json', auth='user')
    def get_sales(self):
        print("Yes here entered")
        patients_rec = request.env['sale.order'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                'name': rec.partner_id.name,
                'date': rec.date_order,
                # 'loc': rec.product_id.name,
                # 'id': rec.company_id,
                # 'uom':rec.product_id.uom_id
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data

# ****
#  picking = self.env['stock.picking'].create({
#             'location_id': self.test_supplier.id,
#             'location_dest_id': self.warehouse_1.wh_input_stock_loc_id.id,
#             'partner_id': self.test_partner.id,
#             'picking_type_id': self.env.ref('stock.picking_type_in').id,
#             'immediate_transfer': False,
#         })
#         move_receipt_1 = self.env['stock.move'].create({
#             'name': self.kit_parent.name,
#             'product_id': self.kit_parent.id,
#             'product_uom_qty': 3,
#             'product_uom': self.kit_parent.uom_id.id,
#             'picking_id': picking.id,
#             'picking_type_id': self.env.ref('stock.picking_type_in').id,
#             'location_id':  self.test_supplier.id,
#             'location_dest_id': self.warehouse_1.wh_input_stock_loc_id.id,
#         })
#         picking.action_confirm()
#
#
