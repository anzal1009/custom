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
    # @http.route('/data/create_rm_purchase', auth='Key', type='json')
    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
        for row in rec["data"]:
            invoice_date = row["master"]["date_approve"]
            print(invoice_date)
            # testeddate =  invoice_date
            # Invoicedate = datetime.strftime(testeddate, '%m/%d/%Y')
            # print(Invoicedate)

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
                    purchase_order_1.button_confirm()
                    # purchase_order_1.date_approve = invoice_date
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            picking.button_validate()
                            # pick_to_backorder = request.env['stock.immediate.transfer']
                            # stock_immediate = pick_to_backorder.create(
                            #     {'pick_ids': [(6, 0, purchase_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                            # stock_immediate.process()
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

        stock_det = request.env['stock.quant'].search([])
        print(stock_det)
        stock = []
        for i in stock_det:
            datas = {
                'location': i.location_id.name,
                'on hand': i.quantity,
                'lot': i.lot_id.name,
                'product id': i.product_id.id,
                'product name': i.product_id.name,
                'uom': i.product_id.uom_id.id,
                'pdt category': i.product_id.categ_id.name,
                # 'quantity':i.product_id.qty_available
            }
            stock.append(datas)
        print("Purchase order--->", stock)
        data = {'status': 200, 'response': stock, 'message': 'Done All Products Returned'}
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
                'opera': rec.picking_type_id,
                'dest': rec.location_dest_id,
                'loca': rec.location_id,
                'name': rec.product_id.name,
                'product_id': rec.product_id,
                'qty': rec.product_uom_qty,
                'uom': rec.product_id.uom_id.id,
                # 'name': rec.product_id.name,
                # 'res':rec.reserved_availability,
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data

    # *****

    @http.route('/create_transfers_inv', type='json', auth='user')
    def action_approve(self, **rec):
        if request.jsonrequest:

            picking_type = request.env['stock.picking.type'].search([])
            print(picking_type)
            for o in picking_type:
                if o.name.startswith('Internal Transfers'):
                    picking_type_id = o.id
                    print(o.id)
                    print(o.name)
                    print(picking_type)

            picking = []
            for record in rec["picking"]:
                picking = request.env['stock.picking'].create({
                    'location_id': record["location"],
                    'location_dest_id': record["location_dest"],
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': o.id,
                    'immediate_transfer': False,
                })
            move_receipt_1 = []
            for line in rec["pick_lines"]:
                location_id = record["location"]
                location_dest_id = record["location_dest"]
                product_id = line["product_id"]
                # print(product_id.uom)

                units = request.env['product.template'].search([])
                print(units)

                move_receipt_1 = request.env['stock.move'].create({
                    'name': line["name"],
                    'product_id': int(product_id),
                    'product_uom_qty': line["qty"],
                    # 'quantity_done': line["qty_done"],
                    'product_uom': 12,
                    'picking_id': picking.id,
                    'picking_type_id': o.id,
                    'location_id': location_id,
                    'location_dest_id': int(location_dest_id),
                })
        if move_receipt_1:
            data = {'status': 'success', 'message': 'Done All Transfers Returned'}

            # record.state = 'approved'
            # record.approved_date = fields.Datetime.now()
            # record.approved_by = request.env.uid
        else:
            raise ValidationError(_("Something went wrong during your Request generation"))
        return data

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


# ***************** Sale and Purchase ****************


    @http.route('/data/create_sale_purchase', type='json', auth='user')
    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
        for row in rec["data"]:
            invoice_date = row["master"]["date_approve"]
            print(invoice_date)
            # testeddate =  invoice_date
            # Invoicedate = datetime.strftime(testeddate, '%m/%d/%Y')
            # print(Invoicedate)

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
                    purchase_order_1.button_confirm()
                    # purchase_order_1.date_approve = invoice_date
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            picking.button_validate()
                            # pick_to_backorder = request.env['stock.immediate.transfer']
                            # stock_immediate = pick_to_backorder.create(
                            #     {'pick_ids': [(6, 0, purchase_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                            # stock_immediate.process()
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })

        so_numbers = []
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
                        # 'account_analytic_id': False,
                        'product_uom_qty': product_line["product_qty"] or 0,
                        # 'qty_received_manual': 0,
                        # 'discount': discount or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["price_unit"] or 0,
                        # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))
            if vendor:
                sale_order_1 = request.env['sale.order'].create({
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
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'poNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
            return po_numbers


