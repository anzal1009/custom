from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


















class SCACustPayments(http.Controller):
    @http.route('/data/SCA/SCACustomerPayment', type='json', csrf=False, auth='public')
    def journal_creation(self, **rec):

        if request.jsonrequest:
            journal_number = []
            # for row in rec["data"]:
            for record in rec["payment"]:

                reference = record["payment_reference"]

                ref = reference and request.env['account.payment'].sudo().search(
                    [('pay_ref', '=', reference)], limit=1) or False

                refe = reference and request.env['account.move'].sudo().search(
                    [('ref', '=', reference), ('move_type', '=', 'entry')], limit=1) or False

                if ref:
                    journal_number.append({
                        'pay_ref': record["payment_reference"],
                        'paymentNumber': ref.id,
                        # 'payment_details.partner_type': Journal_entry.partner_type
                    })

                else:

                    if refe:
                        journal_number.append({
                            'pay_ref': record["payment_reference"],
                            'paymentNumber': refe.id,
                            # 'payment_details.partner_type': Journal_entry.partner_type
                        })

                    else:



                        if record["payment_detail"]:
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
                                cr_acc = "Debtors - Kerala Direct"
                                cr_acc_id = request.env['account.account'].sudo().search(
                                    [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                                dbt_acc = "Cash (Route Expense)"
                                dbt_acc_id = request.env['account.account'].sudo().search(
                                    [('name', '=', dbt_acc), ('company_id', '=', company_id.id)], limit=1) or False
                                journalname = "Receipt (Route -Cash)"
                                journal_id = journalname and request.env['account.journal'].sudo().search(
                                    [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False
                            if payment_type == "bank":
                                cr_acc = "Debtors - Kerala Direct"
                                cr_acc_id = request.env['account.account'].sudo().search(
                                    [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                                bank_name = record["bank_name"]
                                if bank_name == "Bank of Baroda-09650500000821":
                                    dbt_acc = "Bank of Baroda (CC) - 09650500000821"
                                elif bank_name == "Federal Bank-Current - A/c no-10040200029266":
                                    dbt_acc = "Federal Bank-10040200037830"
                                else:
                                    dbt_acc = "Bank of Baroda (CC) - 09650500000821"

                                dbt_acc_id = request.env['account.account'].sudo().search(
                                    [('name', '=', dbt_acc), ('company_id', '=', company_id.id)], limit=1) or False
                                journalname = "Receipt (Route -Bank)"
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
                                elif (payment_detail == "test"):
                                    cr_acc = "Route Test"

                                cr_acc_id = request.env['account.account'].sudo().search(
                                    [('name', 'like', "Cash (Route Expense)"), ('company_id', '=', company_id.id)],
                                    limit=1) or False
                                # dbt_acc = "Route Collection Cash"
                                dbt_acc_id = request.env['account.account'].sudo().search(
                                    [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                                journalname = "Payment -Route Expense"
                                journal_id = journalname and request.env['account.journal'].sudo().search(
                                    [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False
                            partner = "Route Collection"
                            partner_id = request.env['res.partner'].sudo().search(
                                [('name', '=', partner)], limit=1) or False
                            amount = record["amount"]
                            Journal_entry = request.env['account.move'].sudo().create({
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
                                    'name': dbt_acc_id.name + record["customer_code"],
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
                        else:
                            bank_name = record["bank_name"]
                            customer_name = "Route Collection"
                            sale_to_company = record["company_warehouse_code"]
                            if (sale_to_company == 'JOTHIPURAM'):
                                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
                            if (sale_to_company == 'FCTRY'):
                                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                            payment_mode = record["payment_mode"]
                            if payment_mode == "cash":
                                journalname = "Receipt (Route -Cash)"
                            elif payment_mode == "bank":
                                if bank_name == "Bank of Baroda (CC) - 09650500000821":
                                    journalname = "01CR-Bank BOB"
                                elif bank_name == "Federal Bank-10040200037830":
                                    journalname = "02CR-Bank - Federal Bank"
                                else:
                                    journalname = "01CR-Bank BOB"
                            else:
                                journalname = "Receipt (Route -Bank)"

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
                            payment_detail = record["payment_detail"]

                            if payment_mode == "cash":
                                debit_acc_name = "Cash (Route Expense)"
                            elif payment_mode == "bank":
                                if bank_name == "Bank of Baroda (CC) - 09650500000821":
                                    debit_acc_name = "Bank of Baroda (CC) - 09650500000821"
                                elif bank_name == "Federal Bank-10040200037830":
                                    debit_acc_name = "Federal Bank-10040200037830"
                                else:
                                    debit_acc_name = "Federal Bank-10040200037830"

                            debit_account = request.env['account.account'].sudo().search(
                                [('name', 'like', debit_acc_name), ('company_id', '=', to_company_detail2.id)],
                                limit=1) or False
                            credit_account = request.env['account.account'].sudo().search(
                                [('name', '=', "Debtors - Kerala Direct"), ('company_id', '=', to_company_detail2.id)],
                                limit=1) or False

                            payment_details = request.env['account.payment'].sudo().create({
                                'partner_id': customer_id.id,
                                'amount': record["amount"],
                                'date': date,
                                # 'company_id': to_company_detail2.id,
                                # 'ref': record["refe"],
                                'payment_type': record["payment_type"],
                                'pay_ref': record["payment_reference"],
                                'journal_id': journal_id.id,
                                'payment_method_line_id': payment_method_line_id.id

                            })
                            if payment_details:
                                payment_details.button_open_journal_entry()
                                if payment_details.button_open_journal_entry:
                                    for l in payment_details.move_id:
                                        l.line_ids[1].name = "Debtors - Kerala Direct -  " + record["customer_code"]
                                        l.line_ids[0].name = debit_acc_name + " -  " + record["customer_code"]
                                        l.line_ids.analytic_account_id = analytical_id.id
                                        l.line_ids[1].account_id = credit_account.id

                                journal_number.append({
                                    'pay_ref': record["payment_reference"],
                                    'paymentNumber': payment_details.id
                                })

            return journal_number