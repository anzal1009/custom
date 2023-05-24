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

                testeddate = record['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')


                if customer_name:
                    customer_id = customer_name and request.env['res.partner'].sudo().search(
                        [('name', '=', customer_name)], limit=1) or False


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
                'paymentNumber': payment_details.id
            })
        return paymnt_number





# ************************Sales Order****************************

class ScaSalesOrderTest(http.Controller):

    @http.route('/data/create_sca_sales_test',type='json', csrf=False, auth='public')
    def create_rm_sales(self, **rec):
        so_numbers = []
        pdt_details =[]
        for row in rec["data"]:

            invoice_date = row["master"]["date"]

            date = datetime.strptime(invoice_date, '%d/%m/%Y')


            from_company_detail = request.env['res.company'].sudo().search(
                [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False



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

                gst = product_line["cgst"] + product_line["sgst"]
                igst = product_line["igst"]
                tax_variant = False
                if gst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('amount', '=', str(gst)),
                         ('type_tax_use', '=', "purchase"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('amount', '=', str(igst)),
                         ('type_tax_use', '=', "purchase"),
                         ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                if tax_variant:
                    tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                else:
                    tax = False
                if product_item:
                    product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False

                    if not product:
                        pdt_details.append(
                            {
                                'Product': product_item,
                                'status': "Product Not Found"
                            }
                        )
                        # raise ValidationError(_("Product not found"))

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
                        'discount': ((product_line["discount"] * 100)) / ((product_line["product_qty"] * product_line["rate"])) or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["rate"] or 0,
                        'tax_id':tax,
                    }))
                    pdt_details.append(
                        {
                            'Product': product_item,
                            'status': "Product Found"
                        }
                    )
            if vendor:
                sale_order_1 = request.env['sale.order'].sudo().create({
                    'partner_id': vendor.id,
                    'client_order_ref': row["master"]["orderID"] or '',
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    'date_order':date,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id': from_company_detail.id,
                })
                request.env.cr.commit()
            if sale_order_1:
                sale_order_1.action_confirm()
                sale_order_1.date_order = date
                so_numbers.append({
                    'soNumber': sale_order_1.name,
                    'orderID': row["master"]["orderID"]
                })

                return pdt_details
        return so_numbers
#***********************************************************************************************************************************************************************




class CreateSCASalesServer(http.Controller):
    @http.route('/data/SCA/CreateSCASales_server', type='json', csrf=False, auth='public')
    def CreateSCASales(self, **rec):
        so_numbers = []
        for row in rec["data"]:



            vendor_ref = row["master"]["partner_id"]["ref"]
            from_company_detail = request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
            if vendor_ref:
                vendor = vendor_ref and request.env['res.partner'].sudo().search([('ref', '=', vendor_ref)],
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
                        [('amount', '=', str(gst)), ('type_tax_use', '=',"sale"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('amount', '=', str(igst)), ('type_tax_use', '=',"sale"),
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
#                         'discount': discount or 0,
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
#                     'date_order':row["master"]["date_order"] or False,
#                     'date_planned':row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':from_company_detail.id
                })
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
            return so_numbers


#*************************** Warehouse transfer 2 ******************

class WareHouseInternalTransfer(http.Controller):

    @http.route('/warehouse_transfers',  type='json', csrf=False, auth='public')
    def warehouse_transfers(self, **rec):
        transfersNumber = []
        if request.jsonrequest:
            for row in rec["data"]:
                picking = []
                for record in row["picking"]:

                    location_source = record["location_source"]
                    location_destination = record["location_destination"]
                    company_name = "Eastea Chai Private Limited (KL)"

                    company_id = request.env['res.company'].sudo().search(
                        [('name', '=', company_name)], limit=1) or False

                    picking_type = request.env['stock.picking.type'].sudo().search(
                        [('name', '=', 'Internal Transfers'), ('company_id', '=', company_id.id)], limit=1) or False


                    if location_source:
                        location_id = location_source and request.env['stock.location'].sudo().search(
                            [('name', '=', location_source), ('company_id', '=', company_id.id)], limit=1) or False
                        print(location_id.name)
                    if location_destination:
                        location_dest_id = location_destination and request.env['stock.location'].sudo().search(
                            [('name', '=', location_destination), ('company_id', '=', company_id.id)], limit=1) or False
                        print(location_dest_id.name)

                    picking = request.env['stock.picking'].sudo().create({
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                        # 'partner_id': self.test_partner.id,
                        'picking_type_id': picking_type.id,
                        'immediate_transfer': False,
                        'company_id':company_id.id
                    })


                    move_receipt_1 = []
                    for line in row["pick_lines"]:
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

                            move_receipt_1 = request.env['stock.move'].sudo().create({
                                'name': line["name"],
                                'product_id': product.id,
                                'product_uom_qty': line["qty"],
                                # 'quantity_done': line["qty_done"],
                                'product_uom': unit_id,
                                'picking_id': picking.id,
                                'picking_type_id': picking_type.id,
                                'location_id': location_id.id,
                                'location_dest_id': location_dest_id.id,
                            })


                if picking:
                    transfersNumber.append({
                        'transfersNumber': picking.name
                    })
        return transfersNumber


# ********************TRANSFER ***********************


class ScaTransfer(http.Controller):

    @http.route('/sca/transfer', type='json', csrf=False, auth='public')
    def sca_transfers(self, **rec):
        transfersNumber = []
        for row in rec["data"]:
            if request.jsonrequest:
                for record in row["picking"]:
                    # print(record)
                    location_source = record["location_source"]
                    location_destination = record["location_destination"]
                    company_name = "Eastea Chai Private Limited (KL)"

                    company_id = request.env['res.company'].sudo().search(
                        [('name', '=', company_name)], limit=1) or False

                    picking_type = request.env['stock.picking.type'].sudo().search(
                        [('name', '=', 'Internal Transfers'),('company_id', '=', company_id.id)], limit=1) or False

                    if location_source:
                        location_id = location_source and request.env['stock.location'].sudo().search(
                            [('name', 'like', location_source),('company_id', '=', company_id.id)], limit=1) or False
                    if location_destination:
                        location_dest_id = location_destination and request.env['stock.location'].sudo().search(
                            [('name', 'like', location_destination),('company_id', '=', company_id.id)], limit=1) or False


                for line in row["pick_lines"]:
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

                        move_ids_without_package=[]

                        move_ids_without_package.append((0, 0, {
                            'name': line["name"],
                            'product_id': product.id,
                            'product_uom_qty': line["qty"],
                            # 'quantity_done': line["qty_done"],
                            'product_uom': unit_id,
                            # 'picking_id': picking.id,
                            'picking_type_id': picking_type.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                        }))

                        picking = request.env['stock.picking'].sudo().create({
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                            # 'partner_id': self.test_partner.id,
                            'picking_type_id': picking_type.id,
                            'immediate_transfer': False,
                            'move_ids_without_package':move_ids_without_package,
                        })

                    if picking:
                        transfersNumber.append({
                            'transfersNumber': picking.name
                        })
        return transfersNumber


# ***********************stagging transfr********

class WareHouseInternalTransferStagging(http.Controller):

    @http.route('/warehouse_transfers_stagging', type='json', csrf=False, auth='public')
    def warehouse_transfers(self, **rec):
        transfersNumber = []
        if request.jsonrequest:
            for row in rec["data"]:
                picking = []
                for record in row["picking"]:

                    location_source = record["location_source"]
                    location_destination = record["location_destination"]
                    company_name = "Eastea Chai Private Limited (KL)"

                    company_id = request.env['res.company'].sudo().search(
                        [('name', '=', company_name)], limit=1) or False

                    picking_type = request.env['stock.picking.type'].sudo().search(
                        [('name', '=', 'Internal Transfers'), ('company_id', '=', company_id.id)], limit=1) or False

                    location_id = location_source and request.env['stock.location'].sudo().search(
                            [('name', '=', location_source), ('company_id', '=', company_id.id)], limit=1) or False

                    location_dest_id = location_destination and request.env['stock.location'].sudo().search(
                            [('name', '=', location_destination), ('company_id', '=', company_id.id)], limit=1) or False

                    picking = request.env['stock.picking'].sudo().create({
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                        # 'partner_id': self.test_partner.id,
                        'picking_type_id': picking_type.id,
                        'immediate_transfer': False,
                        'company_id': company_id.id
                    })

                move_receipt_1 = []
                for line in row["pick_lines"]:
                    product_item = line["name"]
                    if product_item:
                        product = product_item and request.env['product.product'].sudo().search(
                            [('name', '=', product_item)], limit=1) or False
                        # uom_ids = request.env['uom.uom'].sudo().search([])
                        # unit_id = request.env.ref('uom.product_uom_unit') and request.env.ref(
                        #     'uom.product_uom_unit').id or False
                        # for record in uom_ids:
                        #     if record.name == "kg":
                        #         unit_id = record.id

                        if not product:
                            raise ValidationError(_("Product not found"))

                        move_receipt_1 = request.env['stock.move'].sudo().create({
                            'name': line["name"],
                            'product_id': product.id,
                            'product_uom_qty': line["qty"],
                            # 'quantity_done': line["qty_done"],
                            'product_uom': product.uom_id.id,
                            'picking_id': picking.id,
                            'picking_type_id': picking_type.id,
                            'location_id': location_id.id,
                            'location_dest_id': location_dest_id.id,
                            'company_id': company_id.id
                        })

                if picking:
                    transfersNumber.append({
                        'transfersNumber': picking.name
                    })
        return transfersNumber




######
class WarehouseScaTransfer(http.Controller):
    @http.route('/data/sca_warehouse_transfer', type='json', csrf=False, auth='public')
    def sca_transfer(self,**rec):
        transfernumber=[]
        for row in rec["data"]:

            for record in row["picking"]:
                # location_source = record["location_source"]
                # location_destination = record["location_destination"]
                location_code = record["location_code"]
                destination_code = record["destination_code"]
                company_name = "Eastea Chai Private Limited (KL)"
                reference = record["reference"]


                company_id = request.env['res.company'].sudo().search(
                    [('name', '=', company_name)], limit=1) or False

                picking_type = request.env['stock.picking.type'].sudo().search(
                    [('name', '=', 'Internal Transfers'),('company_id', '=', company_id.id)], limit=1) or False

                location_id =  location_code and request.env['stock.location'].sudo().search(
                    [ ('loc_code', '=', location_code),('company_id', '=', company_id.id)], limit=1) or False

                location_dest_id = destination_code and request.env['stock.location'].sudo().search(
                    [ ('loc_code', '=', destination_code),('company_id', '=', company_id.id)], limit=1) or False


                picking = request.env['stock.picking'].sudo().create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': picking_type.id,
                    'immediate_transfer': False,
                    'ref': " SCA "  +  reference,
                    'company_id': company_id.id
                })

            for line in row["pick_lines"]:
                product_item = line["name"]
                if product_item:
                    product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    if not product:
                        raise ValidationError(_("Product not found"))

                    move_receipt_1 = request.env['stock.move'].sudo().create({
                        'name': line["name"],
                        'product_id': product.id,
                        'product_uom_qty': line["qty"],
                        # 'quantity_done': line["qty_done"],
                        'product_uom': product.uom_id.id,
                        'picking_id': picking.id,
                        'picking_type_id': picking_type.id,
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                        'company_id': company_id.id
                    })

        if picking:
            transfernumber.append({
                'transfersNumber': picking.name
            })
        return transfernumber


##################################

class unlinkStockTransferRecord(http.Controller):

    @http.route('/unlinkStockTransferRecord', type='json', csrf=False, auth='public')
    def unlinkStockTransferRecord(self, **rec):
        recordNumber = rec["recordNumber"]
        print(recordNumber)
        recordNumber = rec["recordNumber"]
        recordData = request.env['stock.picking'].sudo().search([('name', '=', recordNumber)]) or False
        for rec in recordData:
            rec.origin = False
            recordData = request.env['stock.move'].sudo().search([('picking_id', '=', rec.id)]) or False
            for i in recordData:
                i.picking_id = False



class unlinkSaleRecord(http.Controller):

    @http.route('/unlinkSaleRecord', type='json', csrf=False, auth='public')
    def unlinkSaleRecord(self, **rec):
        recordNumber = rec["recordNumber"]
        recordData = request.env['purchase.order'].sudo().search([('name', '=', recordNumber)]) or False
        for rec in recordData:
            # rec.group_id= False
            rec.state = "cancel"
            # recordDatas = request.env['purchase.order.line'].sudo().search([('order_id', '=', rec.id)]) or False
            # for i in recordDatas:
            #     i.qty_received = 0
            #     # i.order_id = False






 #########################################################

class Payments1(http.Controller):
    @http.route('/data/SCA/SCACustomerPayment1', type='json', csrf=False, auth='public')
    def create_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                customer_name = record["name"]
                sale_to_company = record["company_ware_house"]
                if (sale_to_company == 'JOTHIPURAM'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                if (sale_to_company == 'KAVALANGAD'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                journalname = "Route Sale"
                journal_id = journalname and request.env['account.journal'].sudo().search(
                    [('name', '=', journalname), ('company_id', '=', to_company_detail2.id)], limit=1) or False

                testeddate = record['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')

                if customer_name:
                    customer_id = customer_name and request.env['res.partner'].sudo().search(
                        [('ref', '=', customer_name)], limit=1) or False
                    payment_method_line_id = request.env['account.payment.method.line'].sudo().search(
                        [('name', '=', 'Manual')], limit=1) or False

                payment_details = []
                payment_details = request.env['account.payment'].sudo().create({
                    'partner_id': customer_id.id,
                    'amount': record["amount"],
                    'date': date,
                    #                     'company_id': to_company_detail2.id,
                    # 'ref': record["refe"],
                    'payment_type': record["payment_type"],
                    #                     'bank_reference': record["bank"],
                    #                     'cheque_reference': record["cheque"],
                    'pay_ref': record["payment_reference"],
                    'journal_id': journal_id.id,
                    'payment_method_line_id': payment_method_line_id.id

                })
                if payment_details:
                    paymnt_number.append({
                        'pay_ref': record["payment_reference"],
                        'paymentNumber': payment_details.id
                    })
        return paymnt_number




