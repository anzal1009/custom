from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time






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
                journalname="Route Sale"
                journal_id = journalname and request.env['account.journal'].sudo().search(
                        [('name', '=', journalname),('company_id', '=', to_company_detail2.id)], limit=1) or False

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
                    'journal_id':journal_id.id,
                    'payment_method_line_id': payment_method_line_id.id

                })

                if payment_details:
                    for jo in rec["details"]:
                        bata = jo["Batta"]
                        Rent = jo["Rent"]
                        print(bata)
                    payment_details.button_open_journal_entry()
                    # payment_details.action_open_destination_journal()
                    if payment_details.button_open_journal_entry:
                        for l in payment_details.move_id:
                            print(payment_details.move_id)

                            lines = [(2, 0, 0)]
                            for i in l.line_ids:
                                print(l.line_ids)
                                val = {
                                    'partner_id': customer_id.id,
                                    # 'name': bata ,
                                    # 'account_id': 77,


                                }
                                lines.append((0, 0, val))
                                print(lines)
                            l.line_ids = lines



                    paymnt_number.append({
                        'pay_ref': record["payment_reference"],
                        'paymentNumber': payment_details.id
                    })
        return paymnt_number