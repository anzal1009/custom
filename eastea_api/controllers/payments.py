from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _




class Payments(http.Controller):
    @http.route('/create_payments', type='json', csrf=False, auth='public')
    def create_payments(self, **rec):
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
                    'payment_type': record["payment_type"],
                    'bank_reference': record["bank"],
                    'cheque_reference': record["cheque"],
                    'pay_ref': record["payment_reference"]

                })
                if payment_details:
                    paymnt_number.append({
                        'paymentNumber': payment_details.id
                    })
            return paymnt_number

#
# class PaymentRefSync(http.Controller):
#     @http.route('/payment_ref_po_return', type='json', csrf=False, auth='public')
#     def PaymentRefSync(self, **rec):
#         if request.jsonrequest:
#             pynumber = []
#             for record in rec["payment"]:
#                 reference = record["ref"]
#                 payment_reference = request.env['account.payment'].sudo().search([('pay_ref', '=', reference)])
#                 if payment_reference:
#                     pynumber.append({
#                         'PaymentRef': reference,
#                         'PaymentNumber': payment_reference.name
#                     })
#             return pynumber


##Payment Cancellation
class PaymentCancellation(http.Controller):
    @http.route('/payment_cancellation', type='json', csrf=False, auth='public')
    def cancel_payments(self, **rec):
        if request.jsonrequest:
            payment_number = []
            for record in rec["payment"]:
                sale_to_company = "COCHIN"
                if (sale_to_company == 'COIMBATORE'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                if (sale_to_company == 'COCHIN'):
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
