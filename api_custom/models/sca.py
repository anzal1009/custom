from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


################### Payment Sync ######################

class PaymentRefSync(http.Controller):
    @http.route('/data/SCA/payment_ref_po_return', type='json', csrf=False, auth='public')
    def PaymentRefSync(self, **rec):
        if request.jsonrequest:
            pynumber = []
            for record in rec["payment"]:
                reference = record["ref"]
                payment_reference = request.env['account.payment'].sudo().search([('pay_ref', '=', reference)])
                if payment_reference:
                    pynumber.append({
                        'PaymentRef': reference,
                        'PaymentNumber': payment_reference.name,
                        'PaymentNumberStatus': "Updated"
                    })
                if not payment_reference:
                    pynumber.append({
                        'PaymentRef': reference,
                        'PaymentNumber': False,
                        'PaymentNumberStatus': "Not Updated. Reference Number Not Found in ODOO"
                    })
            return pynumber



################# Payment Cancellation ##################

class PaymentCancellation(http.Controller):
    @http.route('/data/SCA/payment_cancellation', type='json', csrf=False, auth='public')
    def cancel_payments(self, **rec):
        if request.jsonrequest:
            payment_number = []
            for record in rec["payment"]:
                sale_to_company = record["company_warehouse_code"]
                #                 sale_to_company = "FCTRY"
                if (sale_to_company == 'COIMBATORE'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                if (sale_to_company == 'FCTRY'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                name = record["name"]
                paymnt_cncl = request.env['account.payment'].sudo().search(
                    [('name', '=', name), ('company_id', '=', to_company_detail2.id)])
                if paymnt_cncl:
                    paymnt_cncl.action_draft()
                    paymnt_cncl.action_cancel()
                    payment_number.append({
                        'PaymentNumber': name,
                        'PaymentStatus': "Cancelled"
                    })
            return payment_number



########################### Payment Creation #########################


class Payments(http.Controller):
    @http.route('/data/SCA/SCACustomerPayment', type='json', csrf=False, auth='public')
    def create_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                customer_name = record["customer_code"]
                sale_to_company = record["company_warehouse_code"]
                if (sale_to_company == 'JOTHIPURAM'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                if (sale_to_company == 'FCTRY'):
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


##################### Warehouse Transfer #################


class WarehouseScaTransfer(http.Controller):

    @http.route('/data/SCA/create_transfers_inv', type='json', csrf=False, auth='public')
    def sca_warehouse_transfer(self, **rec):
        transfernumber = []
        for row in rec["data"]:

            for record in row["picking"]:
                location_code = record["location_code"]
                destination_code = record["destination_code"]
                #                 location_source = record["location_source"]
                #                 location_destination = record["location_destination"]
                reference = record["reference"]
                company_name = "Eastea Chai Private Limited (KL)"

                company_id = request.env['res.company'].sudo().search(
                    [('name', '=', company_name)], limit=1) or False

                picking_type = request.env['stock.picking.type'].sudo().search(
                    [('name', '=', 'Internal Transfers'), ('company_id', '=', company_id.id)], limit=1) or False

                location_id = location_code and request.env['stock.location'].sudo().search(
                    [('loc_code', '=', location_code), ('company_id', '=', company_id.id)], limit=1) or False

                location_dest_id = destination_code and request.env['stock.location'].sudo().search(
                    [('loc_code', '=', destination_code), ('company_id', '=', company_id.id)], limit=1) or False

                picking = request.env['stock.picking'].sudo().create({
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    # 'partner_id': self.test_partner.id,
                    'picking_type_id': picking_type.id,
                    'immediate_transfer': False,
                    'ref': " SCA " + reference,
                    'company_id': company_id.id
                })

            for line in row["pick_lines"]:
                product_item = line["name"]
                print(product_item)
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


# # **************** SCA Stock Transfer Details****************

class SCAStockTransfer(http.Controller):
    @http.route('/data/SCA/GetStockTransfer', type='json', csrf=False, auth='public')
    def SCAStockTransfer(self):
        transfer_rec = request.env['stock.picking'].sudo().search(
            [('location_dest_id.name', 'like', 'Route'), ('state', '=', 'done')])
        transfer = []
        for rec in transfer_rec:
            order_line = []
            for line in rec.move_line_ids_without_package:
                order_line.append({
                    'Product_line_id': line.id,
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'product_code': line.product_id.default_code,
                    'lot_number': line.lot_id.name,
                    'consumed_qty': line.qty_done,
                    'price': line.product_id.list_price,
                    'unit_of_measure': line.product_uom_id.name
                })
            vals = {
                'Master_line_id': rec.id,
                'Transfer_id': rec.name,
                'Transfer_name': rec.picking_type_id.name,
                'destination_location': rec.location_dest_id.name,
                'Destination_location_code': rec.dest_loc_code,
                'source_location': rec.location_id.name,
                'Source_location_code': rec.so_loc_code,
                'line_items': order_line,
                'date_done': rec.date_done,
            }
            transfer.append(vals)
        data = {'status': 200, 'response': transfer, 'message': 'Done. All Products Returned'}
        return data



# ************** SCAItemMaster ***********

class SCAItemMaster(http.Controller):
    @http.route('/data/SCA/ItemMaster', type='json', csrf=False, auth='public')
    def SCAItemMaster(self):
        SCAItemMaster_rec = request.env['product.template'].sudo().search(
            [('categ_id', 'like', "FG"), ('categ_id', '!=', "SFG")])
        SCAItemMaster_data = []
        for rec in SCAItemMaster_rec:
            tax_id = rec.taxes_id
            # print(tax_id)
            taxes = "None"
            if not tax_id:
                TaxRt = 0.0
                SgstRt = 0.0
                CgstRt = 0.0
                IgstRt = 0.0
            if tax_id:
                for i in tax_id:
                    taxes = str(i.name)
                    print(taxes)
                    TaxRt = 0.0
                    SgstRt = 0.0
                    CgstRt = 0.0
                    IgstRt = 0.0
                    if taxes.startswith('GST'):
                        TaxRt = i[0].amount
                        IgstRt = 0.0
                        CgstRt = (TaxRt / 2)
                        SgstRt = (TaxRt / 2)

                    if taxes.startswith('IGST'):
                        TaxRt = i[0].amount
                        IgstRt = TaxRt
                        CgstRt = 0.0
                        SgstRt = 0.0
            vals = {
                'product_code': rec.default_code,
                'product_name': rec.name,
                'sales_price': rec.list_price,
                'uom': rec.uom_id.name,
                'hsn_code': rec.l10n_in_hsn_code,
                'weight': rec.weight,
                'sgst': SgstRt,
                'cgst': CgstRt,
                'igst': IgstRt,

            }
            SCAItemMaster_data.append(vals)
        data = {'status': 200, 'response': SCAItemMaster_data, 'message': 'Success'}
        return data


# **************** SCA Sales ****************

class CreateSCASales(http.Controller):
    @http.route('/data/SCA/CreateSCASales', type='json', csrf=False, auth='public')
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
                    product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
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
                        'discount': ((product_line["discount"] * 100)) / (
                        (product_line["product_qty"] * product_line["rate"])) or 0,
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
                    'company_id': from_company_detail.id
                })
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return so_numbers