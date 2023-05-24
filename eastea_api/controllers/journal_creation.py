from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class Journal(http.Controller):

    @http.route('/journal/creation', type='json', csrf=False, auth='public')
    def journal_creation(self, **rec):

        if request.jsonrequest:
            journal_number = []
            # for row in rec["data"]:
            for record in rec["payment"]:

                company = record["company_warehouse_code"]
                if (company == 'COIMBATORE'):
                    company_id = company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                if (company == 'FCTRY'):
                    company_id = company and request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

                reference = record["payment_reference"]

                testeddate = record['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')

                code = record["customer_code"]
                if code:
                    analytical_id = request.env['account.analytic.account'].sudo().search(
                        [('code', 'like', code), ('company_id', '=', company_id.id)], limit=1) or False
                    if not analytical_id:
                        analytical_details = {
                            'name': code,
                            'code': code,
                            'company_id': company_id.id,
                        }
                        analytical_id = request.env['account.analytic.account'].sudo().create(analytical_details)
                        request.env.cr.commit()
                    analytical_id = request.env['account.analytic.account'].sudo().search(
                        [('code', 'like', code), ('company_id', '=', company_id.id)], limit=1) or False

                payment_type = record['payment_mode']
                if payment_type == "cash":
                    cr_acc = "Kerala Receivables"
                    cr_acc_id = request.env['account.account'].sudo().search(
                        [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                    dbt_acc = "Cash(Route Expense)"
                    dbt_acc_id = request.env['account.account'].sudo().search(
                        [('name', '=', dbt_acc), ('company_id', '=', company_id.id)], limit=1) or False
                    journalname = "Route Collection (Cash)"
                    journal_id = journalname and request.env['account.journal'].sudo().search(
                        [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False
                if payment_type == "bank":
                    cr_acc = "Kerala Receivables"
                    cr_acc_id = request.env['account.account'].sudo().search(
                        [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                    dbt_acc = "Bank Of Baroda"
                    dbt_acc_id = request.env['account.account'].sudo().search(
                        [('name', '=', dbt_acc), ('company_id', '=', company_id.id)], limit=1) or False
                    journalname = "Route Collection (Bank)"
                    journal_id = journalname and request.env['account.journal'].sudo().search(
                        [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False

                payment_details = []

                payment_detail = record["payment_detail"]
                if payment_detail:
                    payment_detail = payment_detail.lower()
                    cr_acc = False
                    if (payment_detail == "additional batta"):
                        cr_acc = "Route Add. Bata"
                    elif (payment_detail == "batta"):
                        cr_acc = "Route Bata"
                    elif (payment_detail == "combo-off / coupons for shops"):
                        cr_acc = "Route Combo/Coupon"
                    elif (payment_detail == "complimentary for shops"):
                        cr_acc = "Route Complimentory for Shop"
                    elif (payment_detail == "fuel"):
                        cr_acc = "Route Vehicle Fuel"
                    elif (payment_detail == "display allowance for shops"):
                        cr_acc = "Route Display Allowance Shop"
                    elif (payment_detail == "hot tea shop bata"):
                        cr_acc = "Route HTS Bata"
                    elif (payment_detail == "medical expense"):
                        cr_acc = "Route Others"
                    elif (payment_detail == "others (specify reason)"):
                        cr_acc = "Route Others"
                    elif (payment_detail == "paper roll"):
                        cr_acc = "Route Others"
                    elif (payment_detail == "parking fees"):
                        cr_acc = "Route Vehicle Expense"
                    elif (payment_detail == "police petty"):
                        cr_acc = "Route Vehicle Expense"
                    elif (payment_detail == "room rent"):
                        cr_acc = "Route Stay Expenses"
                    elif (payment_detail == "sampling activities"):
                        cr_acc = "Route Sampling Expense"
                    elif (payment_detail == "toll"):
                        cr_acc = "Route Vehicle Expense"
                    elif (payment_detail == "travel tickets"):
                        cr_acc = "Route Travel Expense"
                    elif (payment_detail == "vehicle maintenance"):
                        cr_acc = "Route Maintenance Vehicle"

                    cr_acc_id = request.env['account.account'].sudo().search(
                        [('name', 'like',"Cash(Route Expense)"), ('company_id', '=', company_id.id)], limit=1) or False
                    # dbt_acc = "Route Collection Cash"
                    dbt_acc_id = request.env['account.account'].sudo().search(
                        [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                    journalname = "Route Expense"
                    journal_id = journalname and request.env['account.journal'].sudo().search(
                        [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False

                partner = "Route collection"

                partner_id = request.env['res.partner'].sudo().search(
                    [('name', '=', partner)], limit=1) or False
                print(partner_id.name)

                amount = record["amount"]
                # label = record["label"]

                Journal_entry = request.env['account.move'].create({
                    'move_type': "entry",
                    'ref': reference,
                    'date': date,
                    'journal_id': journal_id.id,
                    'company_id': company_id.id,

                    # 'line_ids': order_line
                    'line_ids': [(0, 0, {
                        'name': dbt_acc_id.name + record["customer_code"],
                        'debit': int(amount),
                        'account_id': dbt_acc_id.id,
                        'partner_id': partner_id.id,
                        'analytic_account_id': analytical_id.id
                    }), (0, 0, {
                        'name': cr_acc_id.name + record["customer_code"],
                        'credit': int(amount),
                        'account_id': cr_acc_id.id,
                        'partner_id': partner_id.id,
                        'analytic_account_id': analytical_id.id
                    })]

                })

                if Journal_entry:
                    journal_number.append({
                        'pay_ref': record["payment_reference"],
                        'paymentNumber': Journal_entry.id,
                        # 'payment_details.partner_type': Journal_entry.partner_type
                    })
            return journal_number


class JournalRefSync(http.Controller):
    @http.route('/data/SCA/journal_ref_return', type='json', csrf=False, auth='public')
    def JournalRefSync(self, **rec):
        if request.jsonrequest:
            pynumber=[]
            for record in rec["payment"]:
                reference = record["payment_reference"]
                payment_reference = request.env['account.move'].sudo().search([('ref', '=', reference),('move_type', '=', "entry")], limit=1)

                if payment_reference.name == "/":
                    pynumber.append({
                        'PaymentRef': reference,
                        'PaymentNumber': False,
                        'PaymentNumberStatus': "Payment not Confirmed in ODOO"
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
