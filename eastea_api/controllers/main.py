from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class Purchase(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()




    # ************************ Warehouse_transfer ******************************

# ******************** Stock_details *****************

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
                'uom': i.product_id.uom_id.name,
                'pdt category': i.product_id.categ_id.name,
                # 'quantity':i.product_id.qty_available
            }
            stock.append(datas)
        print("Purchase order--->", stock)
        data = {'status': 200, 'response': stock, 'message': 'Done All Products Returned'}
        return data['response']

# ****************   Inventory_Transfer_details   ******************


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
                'product_id': rec.product_id.id,
                'qty': rec.product_uom_qty,
                'uom': rec.product_id.uom_id.id,
                # 'name': rec.product_id.name,
                # 'res':rec.reserved_availability,
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data



# ****************** Warehouse Internal Transfers ******************



    @http.route('/create_transfers_inv', type='json', auth='user')
    def action_approve(self, **rec):

        trnsNmbr =[]
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
                product_item= line["name"]

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
                    'TrnsfrNumber':picking.name
                })
        return trnsNmbr



# ****************** Get Sales Orders ********************


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
            date = datetime.strptime(invoice_date,'%d/%m/%Y')
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
                    purchase_order_1.date_approve = date
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            picking.button_validate()
                            pick_to_backorder = request.env['stock.immediate.transfer']
                            stock_immediate = pick_to_backorder.create(
                                {'pick_ids': [(6, 0, purchase_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                            stock_immediate.process()
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
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
                return so_numbers,po_numbers





# ******************* Sale Order ***********************



    @http.route('/data/create_rm_sales', type='json', auth='user')
    def create_rm_sales(self, **rec):
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
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
            return so_numbers




# *************** Payment Creation ******************


    @http.route('/create_customer_payments', type='json', auth='user')
    def create_customer_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number=[]
            for record in rec["payment"]:
                customer_name = record["name"]
                print(customer_name)

                testeddate = record['date']
                date = datetime.strptime(testeddate,'%d/%m/%Y')
                print(date)

                if customer_name:
                    customer_id = customer_name and request.env['res.partner'].sudo().search(
                        [('name', '=', customer_name)], limit=1) or False
                    print(customer_id.id)

            payment_details=[]
            payment_details= request.env['account.payment'].create({
                    'partner_id':customer_id.id,
                    'amount': record["amount"],
                    'date':date
                })
            if payment_details:
                paymnt_number.append({
                    'paymntNumber':payment_details.name
                })
            return paymnt_number



# **************** Manufacturing Order ********************

    @http.route('/create_manufacturing_order', type='json', auth='user')
    def create_manufacturing_order(self, **rec):
        mo_number = []

        if request.jsonrequest:

            for orders in rec["values"]:
                product_name = orders["name"]
                bom_name =orders["bom"]
                # print(product_name)

                testeddate = orders['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')
                # print(date)

                if product_name:
                    product_id = product_name and request.env['product.template'].sudo().search(
                        [('name', '=', product_name)], limit=1) or False

                if bom_name:
                    bom_id = bom_name and request.env['mrp.bom'].sudo().search(
                        [('product_tmpl_id', '=', bom_name)], limit=1) or False
                    # print(bom_id.bom_line_ids.product_id.name)
                if not bom_id:
                    raise ValidationError(_("bom not found"))

                modetails = request.env['mrp.production'].create({
                    'product_id': product_id.id,
                    'product_qty': orders["qty"],
                    'qty_producing': orders["qty"],
                    'product_uom_id': product_id.uom_id.id,
                    'date_planned_start': date,
                    'bom_id':bom_id.id
                    # 'move_row_ids': move_raw_ids

                })
                request.env.cr.commit()
                # print(modetails.id)

                items = []
                move_raw_ids = []
                for comp in rec["components"]:
                    item_name = comp["products"]
                    # print(item_name)

                    if item_name:
                        item_id = item_name and request.env['stock.move'].sudo().search(
                            [('name', '=', item_name)], limit=1) or False
                        # print(item_id.name)
                        # print(item_id.location_id.id)
                        # print(item_id.location_dest_id.id)
                        # print(item_id.product_uom.name)




                    line_items = request.env['stock.move'].create({
                        'product_id': item_id.id,
                        'product_uom_qty': comp["qty"],

                        'name': item_id.name,
                        'product_uom': item_id.product_uom.id,
                        'raw_material_production_id':modetails.id,
                        # 'raw_material_production_id':modetails.id,
                        # 'picking_type_id':item_id.picking_type_id.id,
                        'location_id': item_id.location_id.id,
                        'location_dest_id': item_id.location_dest_id.id,
                        'origin': modetails.name

                    })
                    request.env.cr.commit()
                    # print(line_items.id)

        if modetails:
            mo_number.append({
                'M.O Number': modetails.name
            })
            return mo_number


#******************** MO Details ******************

    @http.route('/get_manufacture', type='json', auth='user')
    def get_sales(self):
        print("Yes here entered")
        patients_rec = request.env['mrp.production'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                'name': rec.product_id.name,
                'qty': rec.product_qty,
                'qtyy': rec.product_uom_qty,
                'nnamme': rec.move_raw_ids.product_id.name,
                'uom':rec.move_raw_ids.name,
                # 'bom_id':rec.bom_id.id
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products M O Returned'}
        return data

# *********************** Purchase ***********************

    @http.route('/create_rm_purchase', type='json', auth='user')


    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
        for row in rec["data"]:
            invoice_date = row["master"]["date_approve"]
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
                    'date_order':date,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()

                if purchase_order_1:
                    purchase_order_1.button_confirm()
                    purchase_order_1.date_approve = date
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            picking.button_validate()
                            pick_to_backorder = request.env['stock.immediate.transfer']
                            stock_immediate = pick_to_backorder.create(
                                {'pick_ids': [(6, 0, purchase_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                            stock_immediate.process()
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
                    return po_numbers

















































