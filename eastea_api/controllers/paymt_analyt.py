from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger
from odoo import http
from datetime import datetime



class Payments(http.Controller):
    @http.route('/data/SCA/SCACustomerPayment7', type='json', csrf=False, auth='public')
    def create_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                if record["payment_detail"]:
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
                            [('name', '=', "Route Sales")], limit=1) or False
                        payment_method_line_id = request.env['account.payment.method.line'].sudo().search(
                            [('name', '=', 'Manual')], limit=1) or False

                    code = record["customer_code"]
                    # print(code)
                    if code:
                        #                         route = row["master"]["partner_id"]["name"]
                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        print(analytical_id.id)
                        if not analytical_id:
                            analytical_details = {
                                'name': code,
                                'code': code,
                                'company_id': to_company_detail2.id,
                            }
                            analytical_id = request.env['account.analytic.account'].sudo().create(analytical_details)
                            request.env.cr.commit()
                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False

                    payment_details = []

                    payment_detail = record["payment_detail"]

                    credit_account = request.env['account.account'].sudo().search(
                        [('name', 'like', payment_detail), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                    #                 print(credit_account.name)
                    debit_account = request.env['account.account'].sudo().search(
                        [('name', '=', "Route Collection Cash"), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                    #                 print(debit_account.name)

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
                        payment_details.button_open_journal_entry()
                        if payment_details.button_open_journal_entry:
                            for l in payment_details.move_id:
                                # for i in l.line_ids:
                                print(l.line_ids[0].account_id.id)
                                #     print(i.account_id.name)
                                l.line_ids[1].name = "Route Collection Cash -  " +record["payment_detail"]
                                l.line_ids[0].name = "Route Expense -  " +record["customer_code"] +" - " + record[
                                    "payment_detail"]
                                l.line_ids.analytic_account_id = analytical_id
                                # l.line_ids[0].analytic_account_id = analytical_id

                        paymnt_number.append({
                            'pay_ref': record["payment_reference"],
                            'paymentNumber': payment_details.id
                        })
                else:
                    customer_name = "Route Sales"
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
                            [('name', '=', customer_name)], limit=1) or False
                        payment_method_line_id = request.env['account.payment.method.line'].sudo().search(
                            [('name', '=', 'Manual')], limit=1) or False

                    code = record["customer_code"]
                    # print(code)
                    if code:
                        #                         route = row["master"]["partner_id"]["name"]
                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        print(analytical_id)
                        if not analytical_id:
                            analytical_details = {
                                'name': code,
                                'code': code,
                                'company_id': to_company_detail2.id,
                            }
                            analytical_id = request.env['account.analytic.account'].sudo().create(analytical_details)
                            request.env.cr.commit()
                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False

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
                        payment_details.button_open_journal_entry()
                        if payment_details.button_open_journal_entry:
                            for l in payment_details.move_id:
                                # for i in l.line_ids:
                                print(l.line_ids[0].account_id.id)
                                #     print(i.account_id.name)
                                l.line_ids[1].name = "Route Collection Cash -  " +record["payment_detail"]
                                l.line_ids[0].name = "Route Expense -  " +record["customer_code"] +" - " + record[
                                    "payment_detail"]
                                l.line_ids.analytic_account_id = analytical_id
                                # l.line_ids[0].analytic_account_id = analytical_id



                        paymnt_number.append({
                            'pay_ref': record["payment_reference"],
                            'paymentNumber': payment_details.id
                        })
            return paymnt_number



class PaymentRefSync(http.Controller):
    @http.route('/data/SCA/payment_ref_po_return', type='json', csrf=False, auth='public')
    def PaymentRefSync(self, **rec):
        if request.jsonrequest:
            pynumber=[]
            for record in rec["payment"]:
                reference = record["ref"]
                payment_reference = request.env['account.payment'].sudo().search([('pay_ref', '=', reference)], limit=1)

                if payment_reference.name == "/":
                    pynumber.append({
                        'PaymentRef': reference,
                        'PaymentNumber': "Payment not Confirmed in ODOO",
                        'PaymentNumberStatus': "Not Updated. Reference Number Not Found in ODOO"
                    })


                elif payment_reference:
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