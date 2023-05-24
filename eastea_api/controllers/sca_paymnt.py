from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _




class Payments(http.Controller):
    @http.route('/data/SCA/SCACustomerPayment2', type='json', csrf=False, auth='public')
    def create_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                # customer_name = record["customer_code"]
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

                tax_type = record["tax_type"]
                if tax_type == "INTRA":
                    cust_name = "Route IntraState Sales"
                elif tax_type == "INTER":
                    cust_name = "Route InterState Sales"

                if cust_name:
                    customer_id = cust_name and request.env['res.partner'].sudo().search(
                        [('name', '=', cust_name)], limit=1) or False
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
                    paymnt_number.append({
                        'pay_ref': record["payment_reference"],
                        'paymentNumber': payment_details.id
                    })
        return paymnt_number