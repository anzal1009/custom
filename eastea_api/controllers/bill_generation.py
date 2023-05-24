from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time

class ExpenseBill(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/data/expense_bill', type='json', auth='user')
    def create_expense_bill(self, **rec):
        pay_numbers = []
        purchase_order_1=[]
        for row in rec["data"]:
            invoice_date = row["master"]["bill_date"]

            date = datetime.strptime(invoice_date, '%d/%m/%Y')

            sale_to_company = row["master"]["company_ware_house"]["name"]

            if (sale_to_company == 'COIMBATORE'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (TN)')], limit=1) or False
            if (sale_to_company == 'COCHIN'):
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
                        'phone': row["master"]["partner_id"]["phone"],
                        'email': row["master"]["partner_id"]["email"],
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


                    # analti_acc=line["analytical_account"]
                    # coa = line["chart_of_account"]

                    if (sale_to_company == 'COIMBATORE'):


                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('name', '=', '01JP-CM01'), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        print(analytical_id.id)

                    if (sale_to_company == 'COCHIN'):
                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('name', '=','01KV-CM01'), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        print(analytical_id.id)

                    # coa_id = coa and request.env['account.account'].sudo().search(
                    #     [('name', '=', coa), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                    # print(coa_id.id)




                    invoice_line_ids.append((0, 0, {
                        'display_type': False,
                        'name': label,
                        'price_unit': price,
                        'tax_ids':tax,
                        'analytic_account_id':analytical_id,
                         # 'account_id':coa_id,


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
                    'date':date,
            #         # 'date_planned':row["master"]["date_approve"] or False,
            #         # 'partner_id': self.env.ref('base.main_partner').id,
            #         # 'name': row.INVOICE_NUM or '',
                    'invoice_line_ids': invoice_line_ids,

                })
                request.env.cr.commit()
                if purchase_order_1:
                    purchase_order_1.action_post()
                    request.env.cr.commit()

            pay_numbers.append({
                'PaymentNumber': purchase_order_1.name,
                'orderID': row["master"]["orderID"],
                'PaymentType':row["master"]["payment_type"]
            })
        sorted_payment = []
        if pay_numbers:
            # sorted_payment = []
            for payment_sort in pay_numbers:
                is_existing = False
                index = 0
                for idx ,i in enumerate(sorted_payment) :
                    if payment_sort["orderID"] == i["orderID"]:
                        is_existing = True
                        index = idx
                        print(index)

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
                        # sorted_payment.insert(0,{
                        #     'tbPaymentNumber': payment_sort["PaymentNumber"],
                        # })
                        a=sorted_payment[index];
                        a['tbPaymentNumber']=payment_sort["PaymentNumber"]
                    elif payment_sort["PaymentType"] == 'Lot Money':
                        # sorted_payment.insert(0,{
                        #     'lotPaymentNumber': payment_sort["PaymentNumber"],
                        # })
                        a = sorted_payment[index];
                        a['lotPaymentNumber'] = payment_sort["PaymentNumber"]
        return sorted_payment



