from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class Payments(http.Controller):

    @http.route('/create_customer_sca_payments', type='json', csrf=False, auth='public')
    def create_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                customer_name = record["name"]

                sale_to_company = record["company_ware_house"]
                if (sale_to_company == 'COIMBATORE'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (TN)')], limit=1) or False
                if (sale_to_company == 'COCHIN'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                    print(to_company_detail2.id)

                jounalname="Route Sale"
                # print(jounalname)
                # jounal_id = jounalname and request.env['account.journal'].sudo().search(
                #         [('name', '=', jounalname),('company_id', '=', to_company_detail2.id)], limit=1) or False
                # print(jounal_id.id)

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
                    'payment_method_line_id':2,
                    'company_id': to_company_detail2.id,
                    # 'ref': record["refe"],
                    'payment_type': record["payment_type"],
                    # 'bank_reference': record["bank"],
                    # 'cheque_reference': record["cheque"],
                    'pay_ref': record["payment_reference"],
                    'journal_id':jounalname

                })
        if payment_details:
            paymnt_number.append({
                'paymentNumber': payment_details.id
            })
        return paymnt_number



#******************* Payment Cancellation ******************


class PaymentCancellation(http.Controller):

    @http.route('/payment_cancellation', type='json', csrf=False, auth='public')
    def cancel_payments(self, **rec):

        if request.jsonrequest:
            paymnt_number = []

            for record in rec["payment"]:

                sale_to_company = record["company_ware_house"]
                print(sale_to_company)
                if (sale_to_company == 'COIMBATORE'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (TN)')], limit=1) or False
                if (sale_to_company == 'COCHIN'):
                    to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                print(to_company_detail2.id)
                name = record["name"]
                # print(name)



                paymnt_cncl = request.env['account.payment'].sudo().search([('name', '=', name),('company_id', '=', to_company_detail2.id)])
                print(paymnt_cncl.id)
                if paymnt_cncl:
                    paymnt_cncl.action_draft()
                    paymnt_cncl.action_cancel()
            return paymnt_cncl.state

# ************************** Payment reference  *****************

class PaymentRefCancel(http.Controller):

    # @http.route('/payment_ref_po_return', type='json', csrf=False, auth='public')
    # def payment_ref_cancel(self, **rec):
    #     if request.jsonrequest:
    #         pynumber=[]
    #         for record in rec["payment"]:
    #             reference = record["ref"]
    #             print(reference)
    #
    #             paymnt_refernce = request.env['account.payment'].sudo().search([('pay_ref', '=', reference)])
    #             # print(paymnt_refernce.name)
    #             if paymnt_refernce:
    #                 pynumber.append({
    #                     'PaymentNumber': paymnt_refernce.name
    #                 })
    #             if not paymnt_refernce:
    #                 raise ValidationError(_("Reference not found"))
    #         return pynumber
    class PaymentRefSync(http.Controller):
        @http.route('/payment_ref_po_return', type='json', csrf=False, auth='public')
        def PaymentRefSync(self, **rec):
            if request.jsonrequest:
                pynumber = []
                for record in rec["payment"]:
                    reference = record["ref"]
                    payment_reference = request.env['account.payment'].sudo().search([('pay_ref', '=', reference)])
                    if payment_reference:
                        pynumber.append({
                            'PaymentRef': reference,
                            'PaymentNumber': payment_reference.name
                        })
                    if not payment_reference:
                                raise ValidationError(_("Reference Number not found,Pease check the Ref no:"))
                return pynumber









