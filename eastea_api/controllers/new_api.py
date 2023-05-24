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

            # company_name = row["master"]["company_ware_house"]["name"]
            # print(company_name)
            # company_id = company_name and request.env['res.company'].sudo().search(
            #     [('name', '=', company_name)], limit=1) or False
            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'COIMBATORE'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (TN)')], limit=1) or False
            if (sale_to_company == 'COCHIN'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (KL)')], limit=1) or False
            print(to_company_detail2.id)

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
                    #                     'date_order':row["master"]["date_order"] or False,
                    #                     'date_planned':row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':to_company_detail2.id
                })
                request.env.cr.commit()

                if purchase_order_1:
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return po_numbers


# ****************RawMaterialInternalTransfer****************
class RawMaterialInternalTransfer(http.Controller):
    @http.route('/data/RawMaterialInternalTransfer', type='json', csrf=False, auth='public')
    def RawMaterialInternalTransfer(self, **rec):

        so_numbers = []
        for row in rec["data"]:
            vendor_gst = row["master"]["partner_id"]["gst_no"]


            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'COIMBATORE'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (TN)')], limit=1) or False
            if (sale_to_company == 'COCHIN'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (KL)')], limit=1) or False

            sale_from_company = row["master"]["partner_id"]["name"]
            if (sale_from_company == 'COIMBATORE'):
                from_company_detail = sale_from_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (TN)')], limit=1) or False
                # print(from_company_detail.id)
            if (sale_from_company == 'COCHIN'):
                from_company_detail = sale_from_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (KL)')], limit=1) or False
                # print(from_company_detail.id)

            if vendor_gst:
                vendor = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
                                                                                 limit=1) or False
                # if not vendor:
                #     vendor_details = {
                #         'name': row["master"]["partner_id"]["name"],
                #         'company_type': "company",
                #         'currency_id': 20,
                #         'street': row["master"]["partner_id"]["address"],
                #         'l10n_in_gst_treatment': "regular",
                #         'street2': " ",
                #         'city': " ",
                #         'zip': " ",
                #         'phone': row["master"]["partner_id"]["phone"],
                #         'email': row["master"]["partner_id"]["email"],
                #         'vat': row["master"]["partner_id"]["gst_no"],
                #         # 'parent_id': 1
                #     }
                #     vendor = request.env['res.partner'].sudo().create(vendor_details)
                #     request.env.cr.commit()
            order_line = []

            for product_line in row["child"]:
                product_item = product_line["name"]
                # cgst = product_line["cgst"]
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
                        'tax_id': tax,
                    }))
            if vendor:
                sale_order_1 = request.env['sale.order'].sudo().create({
                    'partner_id':to_company_detail2.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    #                     'date_order':row["master"]["date_order"] or False,
                    #                     'date_planned':row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':from_company_detail.id
                })
                print(to_company_detail2.id)
                print(to_company_detail2.name)
                print(from_company_detail.id)
                print(from_company_detail.name)
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        #                 return so_numbers,po_numbers

        po_numbers = []
        for row in rec["data"]:
            vendor_gst = row["master"]["partner_id"]["gst_no"]

            purchase_to_company = row["master"]["company_ware_house"]["name"]
            if purchase_to_company == 'COIMBATORE':
                purchase_to_company_detail2 = purchase_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (TN)')], limit=1) or False
                # print(purchase_to_company_detail2.id)
                # print(purchase_to_company_detail2.name)
            if purchase_to_company == 'COCHIN':
                purchase_to_company_detail2 = purchase_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (KL)')], limit=1) or False

            purchase_from_company = row["master"]["partner_id"]["name"]
            if purchase_from_company == 'COIMBATORE':
                purchase_from_company_detail = purchase_from_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (TN)')], limit=1) or False
                print('Purchase From')
                # print(purchase_from_company_detail.id)
                print(purchase_from_company_detail.name)
            if purchase_from_company == 'COCHIN':
                purchase_from_company_detail = purchase_from_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'EASTEA CHAI PVT LTD (KL)')], limit=1) or False
            # print(purchase_from_company_detail.id)





            if vendor_gst:
                vendor = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
                                                                                 limit=1) or False
                # if not vendor:
                #     vendor_details = {
                #         'name': row["master"]["partner_id"]["name"],
                #         'company_type': "company",
                #         'currency_id': 20,
                #         'street': row["master"]["partner_id"]["address"],
                #         'l10n_in_gst_treatment': "regular",
                #         'street2': " ",
                #         'city': " ",
                #         'zip': " ",
                #         'phone': row["master"]["partner_id"]["phone"],
                #         'email': row["master"]["partner_id"]["email"],
                #         'vat': row["master"]["partner_id"]["gst_no"],
                #         # 'parent_id': 1
                #     }
                #     vendor = request.env['res.partner'].sudo().create(vendor_details)
                #     request.env.cr.commit()
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
                    #                     'date_order':row["master"]["date_order"] or False,
                    #                     'date_planned':row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':purchase_to_company_detail2.id
                })
                print(purchase_to_company_detail2.id)
                print(purchase_to_company_detail2.name)
                print(purchase_from_company_detail.id)
                print(purchase_from_company_detail.name)
                request.env.cr.commit()

                if purchase_order_1:
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return so_numbers,po_numbers


# ****************InventoryStockData****************
class InventoryStockData(http.Controller):
    @http.route('/data/InventoryStockData', type='json', csrf=False, auth='public')
    def InventoryStockData(self):
        stock_det = request.env['stock.quant'].sudo().search([])
        stock = []
        for i in stock_det:
            StockData = {
                'location': i.location_id.name,
                'on hand': i.quantity,
                'lot': i.lot_id.name,
                'product id': i.product_id.id,
                'product name': i.product_id.name,
                'uom': i.product_id.uom_id.name,
                'pdt category': i.product_id.categ_id.name,
                'id':i.name
                # 'quantity':i.product_id.qty_available
            }
            stock.append(StockData)
        data = {'status': 200, 'response': stock, 'message': 'Done All Products Returned'}
        return data['response']



# *******************************************
