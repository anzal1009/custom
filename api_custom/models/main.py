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


# ****************RawMaterialPurchase****************
class RawMaterialPurchase(http.Controller):
    @http.route('/data/create_rm_purchase', type='json', csrf=False, auth='public')
    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
        for row in rec["data"]:
            vendor_gst = row["master"]["partner_id"]["gst_no"]
            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'JOTHIPURAM'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if (sale_to_company == 'KAVALANGAD'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
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
                        #                         'phone': row["master"]["partner_id"]["phone"],
                        #                         'email': row["master"]["partner_id"]["email"],
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
                        [('company_id', '=', to_company_detail2.id), ('amount', '=', str(gst)),
                         ('type_tax_use', '=', "purchase"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', to_company_detail2.id), ('amount', '=', str(igst)),
                         ('type_tax_use', '=', "purchase"),
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
                            'tracking': 'lot',
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
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    'date_order': row["master"]["date_order"] or False,
                    'date_planned': row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id': to_company_detail2.id
                })
                #                 request.env.cr.commit()

                if purchase_order_1:
                    purchase_order_1.button_confirm()
                    # purchase_order_1.date_approve = date
                    purchase_order_1.action_view_picking()
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return po_numbers



#******************** RMpurchaseDelivery ******************
class RMpurchaseDelivery(http.Controller):
    @http.route('/inv/RMpurchaseDelivery', type='json', csrf=False, auth='public')
    def RMpurchaseDelivery(self, **rec):
        ret_data = []
        for row in rec["data"]:
            poNumber = row["master"]["poNumber"]
            warehouse = row["master"]["company_ware_house"]["name"]
            if (warehouse == 'JOTHIPURAM'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if (warehouse == 'KAVALANGAD'):
                warehouse_data = warehouse and request.env['res.company'].sudo().search(
                [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            purchase_order_1 = request.env['purchase.order'].sudo().search(
                [('company_id', '=', warehouse_data.id), ('name', '=', poNumber)])

            if purchase_order_1:
                purchase_order_1.action_view_picking()
                if purchase_order_1.picking_ids:
                    for picking in purchase_order_1.picking_ids:
                        for product_line in row["child"]:
                            product = product_line["name"] and request.env['product.product'].sudo().search(
                                [('name', '=', product_line["name"])], limit=1) or False
                            if product:
                                for line_ids in picking.move_line_ids:
                                    if product.id == line_ids.product_id.id and product_line["description"] == line_ids.move_id.name and line_ids.move_id.state == "assigned" and line_ids.lot_name == False:
                                        # print(line_ids.lot_name)
                                        product_lot_number = product_line["lot_number"]
                                        qty_done = product_line["qty_done"]
                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number),('product_id', '=', product_line["name"])])
                                        if not lot_no:
                                            print('lot_no lot_no')
                                            lot_number = {
                                                'name': product_lot_number,
                                                'product_id': product.id,
                                                'company_id': warehouse_data.id
                                            }
                                            create_lot_number = request.env['stock.production.lot'].sudo().create(lot_number)
                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', warehouse_data.id), ('name', '=', product_lot_number)])
                                        line_ids.lot_id = lot_no.id
                                        line_ids.lot_name = lot_no.name
                                        line_ids.qty_done = qty_done
                                        if line_ids.qty_done == qty_done:
                                            ret_data.append({
                                                'poNumber': poNumber,
                                                'itemName': line_ids.product_id.name,
                                                'itemDescription': line_ids.move_id.name,
                                                'itemLOT': lot_no.name,
                                                'status': "Success"
                                            })
                                        else:
                                            ret_data.append({
                                                'poNumber': poNumber,
                                                'itemName': product_line["name"],
                                                'itemDescription': product_line["description"],
                                                'itemLOT': product_line["lot_number"],
                                                'status': "Failed"
                                            }
                                            )

                                    elif product.id == line_ids.product_id.id and product_line["description"] == line_ids.move_id.name and line_ids.move_id.state == "assigned" and line_ids.lot_name != False:
                                        ret_data.append({
                                            'poNumber': poNumber,
                                            'itemName': product_line["name"],
                                            'itemDescription': product_line["description"],
                                            'itemLOT': product_line["lot_number"],
                                            'status': "Failed. Please verify the Transaction in Odoo"
                                        }
                                        )

            else:
                ret_data.append({
                    'poNumber': poNumber,
                    'status': "Failed. PO Not Found"
                })
        return ret_data



#******************** RMExpenseBill ******************
class RMExpenseBill(http.Controller):
    @http.route('/data/RMExpenseBill', type='json', csrf=False, auth='public')
    def RMExpenseBill(self, **rec):
        pay_numbers = []
        purchase_order_1=[]
        for row in rec["data"]:
            invoice_date = row["master"]["bill_date"]
            date = datetime.strptime(invoice_date, '%d/%m/%Y')
            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'JOTHIPURAM'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if (sale_to_company == 'KAVALANGAD'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            jounalname =  row["master"]["journal"]
            jounal_id = jounalname and request.env['account.journal'].sudo().search(
                [('name', '=', jounalname), ('company_id', '=', to_company_detail2.id)], limit=1) or False
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
#                         'phone': row["master"]["partner_id"]["phone"],
#                         'email': row["master"]["partner_id"]["email"],
                        'vat': row["master"]["partner_id"]["gst_no"],
                        # 'parent_id': 1
                    }
                    vendor = request.env['res.partner'].sudo().create(vendor_details)
                invoice_line_ids = []
                for line in row["child"]:
                    label = line["name"]
                    price = line["price_unit"]
                    # tax =line["tax"]
                    gst = line["cgst"] + line["sgst"]
                    igst = line["igst"]
                    tax_variant = False
                    if gst:
                        tax_variant = request.env['account.tax'].sudo().search(
                            [('company_id', '=', to_company_detail2.id), ('amount', '=', str(gst)),
                             ('type_tax_use', '=', "purchase"),
                             ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                    if igst:
                        tax_variant = request.env['account.tax'].sudo().search(
                            [('company_id', '=', to_company_detail2.id), ('amount', '=', str(igst)),
                             ('type_tax_use', '=', "purchase"),
                             ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                    if tax_variant:
                        tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                    else:
                        tax = False

                    invoice_line_ids.append((0, 0, {
                        'display_type': False,
                        'name': label,
                        'price_unit': price,
                        'tax_ids':tax,

                    }))
            if vendor:
                reference = str(row["master"]["po_ref"]) + '/' + str(row["master"]["payment_type"]) + '/' +str(row["master"]["payment_reference"])
                purchase_order_1 = request.env['account.move'].sudo().create({
                    'move_type':"in_invoice",
                    'partner_id': vendor.id,
                    'company_id':to_company_detail2.id,
                    'journal_id':jounal_id.id,
                    # 'ref':reference,
            #         # 'partner_ref': row.SALES_ORDER_NUMBER or '',
            #         # 'origin': row.INVOICE_NUM or '',
                    'invoice_date':date,
#                     'date':date,
            #         # 'date_planned':row["master"]["date_approve"] or False,
            #         # 'partner_id': self.env.ref('base.main_partner').id,
            #         # 'name': row.INVOICE_NUM or '',
                    'invoice_line_ids': invoice_line_ids,

                })
                request.env.cr.commit()
                if purchase_order_1:
#                     purchase_order_1.date = date
                    purchase_order_1.action_post()
                    request.env.cr.commit()

            pay_numbers.append({
                'PaymentNumber': purchase_order_1.name,
                'orderID': row["master"]["orderID"],
                'PaymentType':row["master"]["payment_type"]
            })
        sorted_payment = []
        if pay_numbers:
            for payment_sort in pay_numbers:
                is_existing = False
                index = 0
                for idx ,i in enumerate(sorted_payment) :
                    if payment_sort["orderID"] == i["orderID"]:
                        is_existing = True
                        index = idx
                if is_existing == False:
                    if payment_sort["PaymentType"] == 'Tea Board Charges':
                        sorted_payment.append({
                            'orderID': payment_sort["orderID"],
                            'tbPaymentNumber': payment_sort["PaymentNumber"]
                        })
                    elif payment_sort["PaymentType"] == 'Lot Money':
                        sorted_payment.append({
                            'orderID': payment_sort["orderID"],
                            'lotPaymentNumber': payment_sort["PaymentNumber"]
                        })
                else:
                    if payment_sort["PaymentType"] == 'Tea Board Charges':
                        a=sorted_payment[index];
                        a['tbPaymentNumber']=payment_sort["PaymentNumber"]
                    elif payment_sort["PaymentType"] == 'Lot Money':
                        a = sorted_payment[index];
                        a['lotPaymentNumber'] = payment_sort["PaymentNumber"]
        return sorted_payment



# ******************** MO Details ******************
class GetMODetails(http.Controller):
    @http.route('/data/GetMODetails', type='json', csrf=False, auth='public')
    def get_manufacture(self):
        mo_rec = request.env['mrp.production'].sudo().search([('state', '=', 'done')])
        mo_details = []
        for rec in mo_rec:

            order_lines = []
            for line in rec.move_raw_ids:
                order_lines.append({
                    'consumed_product': line.product_id.name,
                    'consumed_qty': line.product_uom_qty,
                    'lot': line.move_line_ids.lot_id.name,
                    # 'done_qty':line.quantity_done
                })

            vals = {
                # 'id': rec.partner_id,
                'manufacturing_order_no': rec.name,
                'product_name': rec.product_id.name,
                'qty': rec.product_qty,
                'blend': rec.blend,
                # 'bom_id':rec.b,om_id.id,
                'date': rec.date_planned_start,
                'line_items': order_lines,
            }
            mo_details.append(vals)
        data = {'status': 200, 'response': mo_details, 'message': 'Done All Products M O Returned'}
        return data



# ****************RawMaterialInternalTransfer****************
class RawMaterialInternalTransfer(http.Controller):
    @http.route('/data/RawMaterialInternalTransfer', type='json', csrf=False, auth='public')
    def RawMaterialInternalTransfer(self, **rec):
        so_numbers = []
        for row in rec["data"]:
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
                        product_details = {
                            'name': product_line["name"],
                            # 'default_code': row.ITEM_NUM,
                            'list_price': product_line["rate"],
                            # 'l10n_in_hsn_code': row.HSN_CODE,
                            'uom_id': unit_id,
                            'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'tracking': 'lot',
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
                    'date_order': row["master"]["date"] or False,
                    #                     'date_planned':row["master"]["date"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    #                     invoice_date = row["master"]["date"]
                    'order_line': order_line,
                    'company_id': from_company_detail.id
                })
                #                 request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    sale_order_1.date_order = row["master"]["date"]
                    if sale_order_1.picking_ids:
                        sale_order_1.picking_ids.action_toggle_is_locked()
                        for picking in sale_order_1.picking_ids:
                            for line_ids in picking.move_line_ids:
                                line_ids.unlink()
                        for picking in sale_order_1.picking_ids:
                            for product_line in row["child"]:
                                product_lot_number = product_line["lot_number"]
                                product = product_line["name"] and request.env['product.product'].sudo().search(
                                    [('name', '=', product_line["name"])], limit=1) or False
                                lot_no = request.env['stock.production.lot'].sudo().search(
                                    [('company_id', '=', from_company_detail.id), ('name', '=', product_lot_number)])
                                if product:
                                    move_line = request.env['stock.move.line'].sudo().create({
                                        'picking_id': picking.id,
                                        'product_id': product.id,
                                        'product_uom_id': product.uom_id.id,
                                        'qty_done': product_line["product_qty"],
                                        'lot_id': lot_no.id,
                                        'location_id': picking.location_id.id,
                                        'location_dest_id': picking.location_dest_id.id,
                                        'reference': picking.name
                                    })
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
                        [('company_id', '=', purchase_to_company_detail2.id), ('amount', '=', str(gst)),
                         ('type_tax_use', '=', "purchase"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', purchase_to_company_detail2.id), ('amount', '=', str(igst)),
                         ('type_tax_use', '=', "purchase"),
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
                            'tracking': 'lot',
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
                    'date_order': row["master"]["date"] or False,
                    'date_planned': row["master"]["date"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id': purchase_to_company_detail2.id
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



# ****************InventoryStockData****************
class InventoryStockData(http.Controller):
    @http.route('/data/InventoryStockData', type='json', csrf=False, auth='public')
    def InventoryStockData(self):
        stock_det = request.env['stock.quant'].sudo().search([])
        stock = []
        for i in stock_det:
            if (i.quantity > 0 and (i.location_id.name == "Stock" or i.location_id.name == "Raw Material Storage")):
                #                 is_new_item = True
                #                 for j in stock:
                #                     if(j['lot'] == i.lot_id.name):
                #                         j['on hand'] += i.quantity
                #                         is_new_item = False
                #                 if(is_new_item):
                StockData = {
                    'location': i.location_id.name,
                    'on hand': i.quantity,
                    'lot': i.lot_id.name,
                    'product id': i.product_id.id,
                    'product name': i.product_id.name,
                    'uom': i.product_id.uom_id.name,
                    'pdt category': i.product_id.categ_id.name,
                    # 'quantity':i.product_id.qty_available
                }
                stock.append(StockData)

        data = {'status': 200, 'response': stock, 'message': 'Done All Products Returned'}
        return data['response']