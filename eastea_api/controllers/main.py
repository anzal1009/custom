from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class ValuationDateUpdate(http.Controller):
    @http.route('/mo/valuation/date', type='json', csrf=False, auth='public')
    def valuation_date_update(self, **rec):
        for raw in rec["data"]:
            mo_no = raw["number"]
            testeddate = raw['date']
            date = datetime.strptime(testeddate, '%d/%m/%Y')
            print(date)
            val_id = request.env['stock.valuation.layer'].sudo().search([('id', '=', mo_no)]) or False
            print(val_id.create_date)
            print(val_id.description)
            val_id.create_date =  date
            for mo in val_id:
                mo.create_date =date




class AssetsConfirm(http.Controller):
    @http.route('/assets/confirm', type='json', csrf=False, auth='public')
    def assets_confirm(self, **rec):

        assets = request.env['account.asset.asset'].sudo().search([('state', '=', 'draft')], order='id DESC', limit=2) or False

        print(assets)
        # for i in assets:
        #     if i.date <= datetime(2022, 4, 1).date():
        #         try:
        #             i.validate()
        #             request.env.cr.commit()
        #         except Exception:
        #             raise Exception(_("Error"))





class ValuationUnlink(http.Controller):
    @http.route('/mo/valuation/unlink', type='json', csrf=False, auth='public')
    def valuation_unlink(self, **rec):
        for raw in rec["data"]:
            mo_no = raw["number"]
            val_id = request.env['stock.valuation.layer'].sudo().search([('description', 'like', mo_no)]) or False
            # val_id = request.env['mrp.production'].sudo().search([('name', '=', mo_no)]) or False
            for mo in val_id:
                # mo.unlink()
                mo.value =0.00
                # mo.action_view_stock_valuation_layers()
                # print(mo.name)
                # print(mo.move_raw_ids + mo.move_finished_ids + mo.scrap_ids.move_id)
                # for mo in val_id:
                #     # mo.action_view_stock_valuation_layers()







class PoTransferJournal(http.Controller):
    @http.route('/journal/date/change', type='json', csrf=False, auth='public')
    def transfer_jo_date(self, **rec):
        for raw in rec["data"]:
            po_no = raw["number"]
            po_id = request.env['purchase.order'].sudo().search([('name','=',po_no)]) or False
            for pur in po_id:
                if pur.picking_ids:
                    for picking in pur.picking_ids:
                        print(picking.name)
                        picking_name = picking.name
                        print(picking_name)
                        journal = request.env['account.move'].sudo().search([('ref','like',picking_name)]) or False
                        print(journal)
                        for jo in journal:
                            jo.button_draft()
                            jo.name=""
                            jo.date = picking.date_done
                            jo.action_post()








class MoDetails(http.Controller):
    @http.route('/mo_details_updte', type='json', csrf=False, auth='public')
    def mo_details_update(self, **rec):
        for raw in rec["data"]:
            po_no = raw["number"]

            po_id = request.env['mrp.production'].sudo().search([('state','=',po_no)]) or False

            for pur in po_id:
                if pur.picking_ids:
                    print(pur.picking_ids)
                    # for picking in pur.picking_ids:
                    #     print(picking.name)

            









class JournalMoveToDraft(http.Controller):
    @http.route('/journal_reset_to_draft', type='json', csrf=False, auth='public')
    def po_cancellation(self, **rec):
        for raw in rec["data"]:
            print(raw)
            # jo_number = raw["number"]
            # journal =request.env['purchase.order'].sudo().search([('name','=',jo_number)]) or False
            # for j in journal:
            #     j.sudo().button_draft()



class StockValUpdate(http.Controller):
    @http.route('/stock/val/update', type='json', csrf=False, auth='public')
    def cost_update(self, **rec):
        # product_name = rec["name"]
        product_id = request.env['product.product'].sudo().search([]) or False

        for pd in product_id:
            stock_layer = request.env['stock.valuation.layer'].sudo().search([('product_id','=',pd.id)]) or False
            if stock_layer:
                for stk_val in stock_layer:
                    stk_val.action_done()




class StockCostUpdate(http.Controller):
    @http.route('/11/stock/cost/update', type='json', csrf=False, auth='public')
    def cost_update(self, **rec):
        product = request.env['product.product'].sudo().search([]) or False
        for pdt in product:
            if pdt.id:
                lot_number = request.env['stock.production.lot'].sudo().search([('product_id','=',pdt.id)]) or False
                if lot_number:
                    for lot in lot_number:
                        stock_layer = request.env['stock.valuation.layer'].sudo().search([('lot_name_id','=',lot.id)]) or False
                        # print(stock_layer)
                        lot_cost = lot.lot_cost
                        if stock_layer:
                            for stk in stock_layer:
                                # stk.cost = lot.lot_cost
                                print(lot_cost)







class MoMoveUpdate(http.Controller):
    @http.route('/mo/update', type='json', csrf=False, auth='public')
    def mo_update(self, **rec):
        mo_number = rec.name
        mo_details= request.env['mrp.production'].sudo().search(['name','=',mo_number]) or False
        if mo_details:

            mo_move_line = request.env['stock.move'].sudo().create({
                #                                         'picking_id': lot.picking_id.id,
                'product_id': mo_details.product_id.id,
                'product_uom': mo_details.product_id.uom_id.id,
                'product_uom_qty': mo_details.product_qty,
                #                                         'lot_id': lot_no.id,
                'location_id': 33,
                'location_dest_id': 49,
                #                                         'reference': op_type_id.name,
                'company_id': 3,
                'production_id': mo_details.id,
                'name': "New"
            })





class MoFinishedDate(http.Controller):
    @http.route('/date/finished', type='json', csrf=False, auth='public')
    def finished_date(self, **rec):

        mo_details = request.env['mrp.production'].sudo().search([]) or False
        for mo in mo_details:
            # try:
            if mo.state == 'done':
                print(mo.date_planned_start)
                if mo.date_planned_start:
                    mo.date_planned_start = mo.date_finished
            # except Exception:
            #     print("error")



class AssetsDraft(http.Controller):
    @http.route('/assets/draft', type='json', csrf=False, auth='public')
    def assets_draft(self, **rec):

        assets =request.env['account.asset.asset'].sudo().search([]) or False
        for a in assets:
            try:
                a.sudo().set_to_draft()
            except Exception:
                print('Error')


class AssetsConfirm(http.Controller):
    @http.route('/assets/confirm', type='json', csrf=False, auth='public')
    def assets_draft(self, **rec):

        for record in rec["payment"]:
            journal_number = []
            reference = record["payment_reference"]
            type = record["payment_type"]

            ref = reference and request.env['account.payment'].sudo().search(
                [('ref', '=', reference)], limit=1) or False

            print(ref.name)

            if type == "outbound":

                ref = reference and request.env['account.move'].sudo().search(
                    [('ref', '=', reference), ('move_type', '=', 'entry')], limit=1) or False

                print(ref.name)


            if ref :
                print("found")
                journal_number.append({
                    'pay_ref': record["payment_reference"],
                    'paymentNumber': ref.id,
                    # 'payment_details.partner_type': Journal_entry.partner_type
                })
        return journal_number

        # assets =request.env['account.asset.asset'].sudo().search([]) or False
        # for a in assets:
        #     if a.state== 'draft':
        #         try:
        #             a.sudo().validate()
        #         except Exception:
        #             print('Error')





class SCACustPayments(http.Controller):
    @http.route('/data/SCA/SCACustomerPayment/new', type='json', csrf=False, auth='public')
    def journal_creation(self, **rec):

        if request.jsonrequest:
            journal_number = []
            # for row in rec["data"]:
            for record in rec["payment"]:

                reference = record["payment_reference"]

                ref = reference and request.env['account.payment'].sudo().search(
                            [('ref', '=', reference)], limit=1) or False

                if ref:
                    journal_number.append({
                        'pay_ref': record["payment_reference"],
                        'paymentNumber': ref.id,
                        # 'payment_details.partner_type': Journal_entry.partner_type
                    })

                else:
                    journal_number.append({
                        'pay_ref': record["payment_reference"],
                        'msg':"create new pymnt",
                        # 'payment_details.partner_type': Journal_entry.partner_type
                    })




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
                            cr_acc = "Kerala Receivables"
                            cr_acc_id = request.env['account.account'].sudo().search(
                                [('name', '=', cr_acc), ('company_id', '=', company_id.id)], limit=1) or False
                            dbt_acc = "Cash (Route Expense)"
                            dbt_acc_id = request.env['account.account'].sudo().search(
                                [('name', '=', dbt_acc), ('company_id', '=', company_id.id)], limit=1) or False
                            journalname = "Receipt (Route -Cash)"
                            journal_id = journalname and request.env['account.journal'].sudo().search(
                                [('name', '=', journalname), ('company_id', '=', company_id.id)], limit=1) or False
                        if payment_type == "bank":
                            cr_acc = "Kerala Receivables"
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
                            [('name', '=', "Kerala Receivables"), ('company_id', '=', to_company_detail2.id)],
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
                                    l.line_ids[1].name = "Kerala Receivables -  " + record["customer_code"]
                                    l.line_ids[0].name = debit_acc_name + " -  " + record["customer_code"]
                                    l.line_ids.analytic_account_id = analytical_id.id
                                    l.line_ids[1].account_id = credit_account.id

                            journal_number.append({
                                'pay_ref': record["payment_reference"],
                                'paymentNumber': payment_details.id
                            })

            return journal_number






# ################################# NEWW ##############################

class GetMODetail2(http.Controller):
    @http.route('/data/GetMODetails2', type='json', csrf=False, auth='public')
    def get_manufacture(self,**rec):

        for raw in rec["data"]:
            mo_number = raw["number"]
            mo_rec = request.env['mrp.production'].sudo().search([('name','=',mo_number)])
            mo_details = []
            for rec in mo_rec:

                order_lines = []
                for line in rec.move_raw_ids:
                   for l in line.move_line_ids:
                    order_lines.append({
                        'consumed_product': l.product_id.name,
                        'consumed_qty': l.qty_done,
                        'lot':l.lot_id.name,
                        # 'done_qty':line.quantity_done
                    })

                vals = {
                    # 'id': rec.partner_id,
                    'manufacturing_order_no': rec.name,
                    'product_name': rec.product_id.name,
                    'qty': rec.product_qty,
                    'blend': rec.blend,
                    'state' : rec.state,
                    # 'bom_id':rec.b,om_id.id,
                    'date': rec.date_planned_start,
                    'line_items': order_lines,
                }
                mo_details.append(vals)
        data = {'status': 200, 'response': mo_details, 'message': 'Done All Products M O Returned'}
        return data



class InvoiceConfirm(http.Controller):
    @http.route('/invoice/confirm', type='json', csrf=False, auth='public')
    def InvoiceConfirm(self, **rec):
        for raw in rec["data"]:
            inv_number = raw["number"]

            invoice= request.env['account.move'].sudo().search([('move_type', '=', 'entry'),('name', '=',inv_number)])

            for datas in invoice:
                datas.action_post()


class JournalEditor(http.Controller):
    @http.route('/journal/editor', type='json', csrf=False, auth='public')
    def journal_editor(self, **rec):
        for raw in rec["data"]:
            mo_number = raw["mo_number"]

            journal = request.env['account.move'].sudo().search([('move_type', '=', 'entry'),('ref', 'like', mo_number)])

            for datas in journal:
                # print(datas)

                # if journal:
                #     print(journal.name)
                if datas.state == "posted":
                    for draft in datas:
                        draft.button_draft()

                        acc1 = draft.line_ids[0].account_id.id
                        acc2 = draft.line_ids[1].account_id.id

                        account1 = request.env['account.account'].sudo().search([('id', '=', acc1)])

                        account2 = request.env['account.account'].sudo().search([('id', '=', acc2)])



                        for line in draft.line_ids:
                            if line.account_id.id == account1.id:
                                line.account_id = account2.id
                            else:
                                line.account_id = account1.id

                elif datas.state == "draft":
                    # print(journal.state)

                    for drafts in datas:
                        # print(draft)

                        accs1 = drafts.line_ids[0].account_id.id
                        accs2 = drafts.line_ids[1].account_id.id

                        accounts1 = request.env['account.account'].sudo().search([('id', '=', accs1)])

                        accounts2 = request.env['account.account'].sudo().search([('id', '=', accs2)])



                        for line in drafts.line_ids:
                            if line.account_id.id == accounts1.id:
                                line.account_id = accounts2.id
                            else:
                                line.account_id = accounts1.id



















class MoActionButton(http.Controller):
    @http.route('/inv/MoActionButton', type='json', csrf=False, auth='public')
    def mo_button_change(self, **rec):
        for row in rec["data"]:
            moNumber = row["moNumber"]
            mo = request.env['mrp.production'].sudo().search([('name', '=', moNumber)])
            if mo:
                for action in mo:
                    action.action_cost2()
                    request.env.cr.commit()
                    action.compute_mrp_cost()


#
#
# class MoActionButton(http.Controller):
#     @http.route('/mo/action/button', type='json', csrf=False, auth='public')
#     def mo_action_button(self, **rec):
#         mo = request.env['mrp.production'].sudo().search([]) or False
#         for action in mo:
#             action.action_cost2()
#             action.compute_mrp_cost()
#




class MoTransferDate(http.Controller):
    @http.route('/mo/date/transfer/change', type='json', csrf=False, auth='public')
    def mo_date_changer(self, **rec):
        for row in rec["data"]:
            moNumber = row["Mo"]
            modate = row["date"]
            date = datetime.strptime(modate,'%Y-%m-%d')
            mo = request.env['mrp.production'].sudo().search([('name', '=', moNumber)]) or False
            if mo:
                mo.date_planned_start = date
            mo_transfer =request.env['stock.picking'].sudo().search([('origin','=',"MO Transfer " + moNumber)]) or False
            if mo_transfer:
                for d in mo_transfer:
                    if (d.date_done):
                        if (d.state != "done"):
                            d.scheduled_date = date
                        if (d.state == "done"):
                            d.date_done = date
                    for line_ids in d.move_line_ids:
                        line_ids.date = date
                        line_ids.move_id.date = date



class POMoveToCancel(http.Controller):
    @http.route('/5522668/PO_reset_to_draft/po/', type='json', csrf=False, auth='public')
    def po_cancellation(self, **rec):
        poNumber = rec["poNumber"]
        print(poNumber)
        po_bill =request.env['purchase.order'].sudo().search([('name','=',poNumber)]) or False
        for bill in po_bill:
            print(po_bill.name)

            bill.sudo().button_cancel()


class Purchase(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    # ************************ Warehouse_transfer ******************************

class JournalDateChanger(http.Controller):
    @http.route('/Journaldate', type='json', csrf=False, auth='public')
    def Journaldate(self):
        acc = request.env['account.move'].sudo().search([('name', 'like', 'B2RS/2022')]) or False
        for i in acc:
            date = i.invoice_date
            i.date = date
            print(i.date)


            #
            # monumber = row["Mo"]
            # print(monumber)
            #
            # if MO:
            #     for i in MO:
            #         i.state = "draft"




class MODraft(http.Controller):
    @http.route('/MoDraft', type='json', csrf=False, auth='public')
    def MODraft(self, **rec):
        for row in rec["data"]:
            monumber = row["Mo"]
            MO = request.env['mrp.production'].sudo().search([('name', '=', monumber)]) or False
            if MO:
                for i in MO:
                    if i.state =="cancel":
                        for item in i.move_raw_ids:
                            for line in item.move_line_ids:
                                line.qty_done = 0
                                # line.state = "draft"

class UpdateHsn(http.Controller):
    @http.route('/hsncode', type='json', csrf=False, auth='public')
    def hsncode(self, **rec):

        product = rec["product"]
        hsn = rec["hsn"]
        print(product)
        productData = request.env['product.template'].sudo().search([('name', '=', product)]) or False
        if productData:
            productData.l10n_in_hsn_code = hsn

    # ******************** Stock_details *****************

class unlinkStockTransferRecord11(http.Controller):
    @http.route('/unlinkStockTransferRecord11', type='json', csrf=False, auth='public')
    def unlinkStockTransferRecord11(self, **rec):
        recordNumber = rec["recordNumber"]
        print(recordNumber)
        recordNumber = rec["recordNumber"]
        recordData = request.env['stock.picking'].sudo().search([('name', '=', recordNumber)]) or False
        for rec in recordData:
            rec.origin = False
            recordData = request.env['stock.move'].sudo().search([('picking_id', '=', rec.id)]) or False
            for i in recordData:
                i.picking_id = False





    @http.route('/get_products', type='json', auth='user')
    def get_products(self):
        print("Yes here entered")

        stock_det = request.env['stock.quant'].search([])
        print(stock_det)
        stock = []
        for i in stock_det:
            datas = {
                'location': i.location_id.name,
                'on hand': i.quantity,
                'lot': i.lot_id.name,
                'product id': i.product_id.id,
                'product name': i.product_id.name,
                'uom': i.product_id.uom_id.name,
                'pdt category': i.product_id.categ_id.id,
                # 'quantity':i.product_id.qty_available
            }
            stock.append(datas)
        print("Purchase order--->", stock)
        data = {'status': 200, 'response': stock, 'message': 'Done All Products Returned'}
        return data['response']

    # ****************   Inventory_Transfer_details   ******************

    @http.route('/get_transfer', type='json', auth='user')
    def get_transfers(self):
        print("Yes here entered")
        transfer_rec = request.env['stock.picking'].sudo().search([('location_dest_id.name', 'like', 'SCA'),('state', '=', 'done')])
        transfer = []
        for rec in transfer_rec:
            order_line=[]
            for line in rec.move_line_ids_without_package:
                order_line.append({
                    'Product_line_id':line.id,
                    'Product_id':line.product_id.id,
                    'Product_name':line.product_id.name,
                    'Lot_number': line.lot_id.name,
                    'Consumed_qty': line.qty_done,
                    'Price':line.product_id.list_price,
                    'Unit_of_measure':line.product_uom_id.name

                    # 'done_qty':line.quantity_done
                })
            vals = {
                'Transfer_id':rec.name,
                'Master_line_id':rec.id,
                'Transfer_name': rec.picking_type_id.name,
                'Destination_location_name': rec.location_dest_id.name,
                'Destination_location_code': rec.dest_loc_code,
                'Source_location_name': rec.location_id.name,
                'Source_location_code': rec.so_loc_code,
                'Date_done': rec.date_done,
                # 'scheduled_date': rec.scheduled_date,
                # 'source_doc_no': rec.origin,
                'line_items': order_line,
            }
            transfer.append(vals)
        # print("Transfer Completed--->", transfer)
        data = {'status': 200, 'response': transfer, 'message': 'Done All Products Returned'}
        return data

    # ****************** Warehouse Internal Transfers ******************

    @http.route('/create_transfers_inv', type='json', auth='user')
    def action_approve(self, **rec):

        trnsNmbr = []
        if request.jsonrequest:
            for row in rec["data"]:

                picking_type = request.env['stock.picking.type'].sudo().search(
                    [('name', '=', 'Internal Transfers')], limit=1) or False
                picking = []

                for record in row["picking"]:
                    location_source = record["location_source"]
                    location_destination = record["location_destination"]

                    if location_source:
                        location_id = location_source and request.env['stock.location'].sudo().search(
                            [('name', '=', location_source)], limit=1) or False
                        location_dest_id = location_destination and request.env['stock.location'].sudo().search(
                            [('name', '=', location_destination)], limit=1) or False

                    picking = request.env['stock.picking'].create({
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                        # 'partner_id': self.test_partner.id,
                        'picking_type_id': picking_type.id,
                        'immediate_transfer': False,
                    })
                move_receipt_1 = []
                for line in row["pick_lines"]:
                    location_name = location_id
                    location_dest_id = location_dest_id
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

                    move_receipt_1 = request.env['stock.move'].create({
                        'name': line["name"],
                        'product_id': product.id,
                        'product_uom_qty': line["qty"],
                        # 'quantity_done': line["qty_done"],
                        'product_uom': 12,
                        'picking_id': picking.id,
                        'picking_type_id': picking_type.id,
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                    })

        if picking:
            trnsNmbr.append({
                'TrnsfrNumber': picking.name
            })
        return trnsNmbr

    # ****************** Get Sales Orders ********************

    @http.route('/get_sales', type='json', auth='user')
    def get_sales(self):
        print("Yes here entered")
        patients_rec = request.env['sale.order'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                'name': rec.partner_id.name,
                'date': rec.date_order,
                # 'loc': rec.product_id.name,
                # 'id': rec.company_id,
                # 'uom':rec.product_id.uom_id
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data

    # ***************** Sale and Purchase ****************

    @http.route('/data/create_sale_purchase', type='json', auth='user')
    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
        for row in rec["data"]:
            invoice_date = row["master"]["date_approve"]
            print(invoice_date)
            date = datetime.strptime(invoice_date, '%d/%m/%Y')
            print(date)

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
                            'list_price': product_line["price_unit"],
                            # 'l10n_in_hsn_code': row.HSN_CODE,
                            'uom_id': unit_id,
                            'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'categ_id': 1,
                            'standard_price': product_line["price_unit"],

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
                        'account_analytic_id': False,
                        'product_qty': product_line["product_qty"] or 0,
                        'qty_received_manual': 0,
                        # 'discount': discount or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["price_unit"] or 0,
                        # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))

            if vendor:
                purchase_order_1 = request.env['purchase.order'].create({
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    # 'date_order':row["master"]["date_order"] or False,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()

                if purchase_order_1:
                    purchase_order_1.button_confirm()
                    purchase_order_1.date_approve = date
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            picking.button_validate()
                            pick_to_backorder = request.env['stock.immediate.transfer']
                            stock_immediate = pick_to_backorder.create(
                                {'pick_ids': [(6, 0, purchase_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                            stock_immediate.process()
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })

        so_numbers = []
        for row in rec["data"]:
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
                            'list_price': product_line["price_unit"],
                            # 'l10n_in_hsn_code': row.HSN_CODE,
                            'uom_id': unit_id,
                            'uom_po_id': unit_id,
                            'detailed_type': 'product',
                            'categ_id': 1,
                            'standard_price': product_line["price_unit"],
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
                        # 'discount': discount or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["rate"] or 0,
                        # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))
            if vendor:
                sale_order_1 = request.env['sale.order'].create({
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    # 'date_order':row["master"]["date_order"] or False,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
                return so_numbers, po_numbers

    # ******************* Sale Order ***********************

    @http.route('/data/create_rm_sales', type='json', auth='user')
    def create_rm_sales(self, **rec):
        so_numbers = []
        for row in rec["data"]:
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
                        # 'discount': discount or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["rate"] or 0,
                        # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))
            if vendor:
                sale_order_1 = request.env['sale.order'].create({
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    # 'date_order':row["master"]["date_order"] or False,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    so_numbers.append({
                        'soNumber': sale_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
            return so_numbers

    # *************** Payment Creation ******************

    @http.route('/create_customer_payments', type='json', auth='user')
    def create_customer_payments(self, **rec):
        if request.jsonrequest:
            paymnt_number = []
            for record in rec["payment"]:
                customer_name = record["name"]
                print(customer_name)

                testeddate = record['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')
                print(date)

                if customer_name:
                    customer_id = customer_name and request.env['res.partner'].sudo().search(
                        [('name', '=', customer_name)], limit=1) or False
                    print(customer_id.id)

            payment_details = []
            payment_details = request.env['account.payment'].create({
                'partner_id': customer_id.id,
                'amount': record["amount"],
                'date': date
            })
            if payment_details:
                paymnt_number.append({
                    'paymntNumber': payment_details.name
                })
            return paymnt_number

    # **************** Manufacturing Order ********************

    @http.route('/create_manufacturing_order_demo', type='json', auth='user')
    def create_manufacturing_order_demo(self, **rec):
        mo_number = []

        if request.jsonrequest:

            for orders in rec["values"]:
                product_name = orders["name"]
                bom_name = orders["bom"]
                # print(product_name)

                testeddate = orders['date']
                date = datetime.strptime(testeddate, '%d/%m/%Y')
                # print(date)

                if product_name:
                    product_id = product_name and request.env['product.template'].sudo().search(
                        [('name', '=', product_name)], limit=1) or False

                # if bom_name:
                #     bom_id = bom_name and request.env['mrp.bom'].sudo().search(
                #         [('product_tmpl_id', '=', bom_name)], limit=1) or False
                #     # print(bom_id.bom_line_ids.product_id.name)
                # if not bom_id:
                #     raise ValidationError(_("bom not found"))

                modetails = request.env['mrp.production'].create({
                    'product_id': product_id.id,
                    # 'product_qty': orders["qty"],
                    'qty_producing': orders["qty"],
                    'product_uom_id': product_id.uom_id.id,
                    'date_planned_start': date,
                    # 'bom_id': bom_id.id
                    # 'move_row_ids': move_raw_ids

                })
                request.env.cr.commit()
                # print(modetails.id)

                items = []
                move_raw_ids = []
                for comp in rec["components"]:
                    item_name = comp["products"]
                    # print(item_name)

                    if item_name:
                        item_id = item_name and request.env['stock.move'].sudo().search(
                            [('name', '=', item_name)], limit=1) or False
                        # print(item_id.name)
                        # print(item_id.location_id.id)
                        # print(item_id.location_dest_id.id)
                        # print(item_id.product_uom.name)

                    line_items = request.env['stock.move'].create({
                        'product_id': item_id.id,
                        'product_uom_qty': comp["qty"],

                        'name': item_id.name,
                        'product_uom': item_id.product_uom.id,
                        'raw_material_production_id': modetails.id,
                        # 'raw_material_production_id':modetails.id,
                        # 'picking_type_id':item_id.picking_type_id.id,
                        'location_id': item_id.location_id.id,
                        'location_dest_id': item_id.location_dest_id.id,
                        'origin': modetails.name

                    })
                    request.env.cr.commit()
                    # print(line_items.id)

        if modetails:
            mo_number.append({
                'M.O Number': modetails.name
            })
            return mo_number

    # ******************** PO Automation ******************



    # *********************** Purchase ***********************


    def create_rm_purchase(self, **rec):
        print(rec)
        po_numbers = []
        for row in rec["data"]:
            # invoice_date = row["master"]["date_approve"]
            # print(invoice_date)
            # date = datetime.strptime(invoice_date, '%d/%m/%Y')
            # print(date)

            vendor_gst = row["master"]["partner_id"]["gst_no"]
            # company_name=row["master"]["company_ware_house"]["name"]
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
                        'account_analytic_id': False,
                        'product_qty': product_line["product_qty"] or 0,
                        'qty_received_manual': 0,
                        # 'discount': discount or 0,
                        'product_uom': product.uom_id.id or request.env.ref(
                            'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                        'price_unit': product_line["rate"] or 0,
                        # 'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                    }))

            if vendor:
                purchase_order_1 = request.env['purchase.order'].create({
                    'partner_id': vendor.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    # 'date_order':date,
                    # 'date_planned':row["master"]["date_approve"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                })
                request.env.cr.commit()

                if purchase_order_1:
                    purchase_order_1.button_confirm()
                    # purchase_order_1.date_approve = date
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        for picking in purchase_order_1.picking_ids:
                            picking.button_validate()
                            pick_to_backorder = request.env['stock.immediate.transfer']
                            stock_immediate = pick_to_backorder.create(
                                {'pick_ids': [(6, 0, purchase_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                            stock_immediate.process()
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
                    return po_numbers

# *****************************PAyments***


# @http.route('/create_customer_payments', type='json', auth='user')
#
#
# def create_customer_payments(self, **rec):
#     if request.jsonrequest:
#         paymnt_number = []
#         for record in rec["payment"]:
#             customer_name = record["name"]
#             print(customer_name)
#
#             testeddate = record['date']
#             date = datetime.strptime(testeddate, '%d/%m/%Y')
#             print(date)
#
#             if customer_name:
#                 customer_id = customer_name and request.env['res.partner'].sudo().search(
#                     [('name', '=', customer_name)], limit=1) or False
#                 print(customer_id.id)
#
#         payment_details = []
#         payment_details = request.env['account.payment'].create({
#             'partner_id': customer_id.id,
#             'amount': record["amount"],
#             'date': date
#         })
#         if payment_details:
#             paymnt_number.append({
#                 'paymntNumber': payment_details.name
#             })
#         return paymnt_number

# ****************RawMaterialInternalTransfer****************
class RawMaterialInternalTransfer(http.Controller):
    @http.route('/data/RawMaterialInternalTransfer', type='json', csrf=False, auth='public')
    def RawMaterialInternalTransfer(self, **rec):
        so_numbers = []
        for row in rec["data"]:
            vendor_gst = row["master"]["partner_id"]["gst_no"]
            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'JOTHIPURAM'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'IN Company')], limit=1) or False
            if (sale_to_company == 'KAVALANGAD'):
                to_company_detail2 = sale_to_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'YourCompany')], limit=1) or False

            sale_from_company = row["master"]["partner_id"]["name"]
            if (sale_from_company == 'JOTHIPURAM'):
                from_company_detail = sale_from_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'IN Company')], limit=1) or False
            if (sale_from_company == 'KAVALANGAD'):
                from_company_detail = sale_from_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'YourCompany')], limit=1) or False
            if vendor_gst:
                vendor = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
                                                                                 limit=1) or False
#                 if not vendor:
#                     vendor_details = {
#                         'name': row["master"]["partner_id"]["name"],
#                         'company_type': "company",
#                         'currency_id': 20,
#                         'street': row["master"]["partner_id"]["address"],
#                         'l10n_in_gst_treatment': "regular",
#                         'street2': " ",
#                         'city': " ",
#                         'zip': " ",
#                         'phone': row["master"]["partner_id"]["phone"],
#                         'email': row["master"]["partner_id"]["email"],
#                         'vat': row["master"]["partner_id"]["gst_no"],
#                         # 'parent_id': 1
#                     }
#                     vendor = request.env['res.partner'].sudo().create(vendor_details)
#                     request.env.cr.commit()
            order_line = []
            for product_line in row["child"]:
                product_item = product_line["name"]
                gst = product_line["cgst"] + product_line["sgst"]
                igst = product_line["igst"]
                if gst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', from_company_detail.id), ('amount', '=', str(gst)), ('type_tax_use', '=',"sale"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', from_company_detail.id), ('amount', '=', str(igst)), ('type_tax_use', '=',"sale"),
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
                            'tracking':'lot',
                            'categ_id': 1,
                            'standard_price': product_line["rate"],
                        }
                        add_product = request.env['product.template'].sudo().create(product_details)
                        request.env.cr.commit()
                        product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    if product:
                        product_lot_number = product_line["lot_number"]
                        qty_done = product_line["qty_done"]
                        lot_no = request.env['stock.production.lot'].sudo().search(
                            [('company_id', '=', from_company_detail.id), ('name', '=', product_lot_number)])
                        order_line.append((0, 0, {
                            'display_type': False,
                            # 'sequence': 10,
                            'product_id': product.id,
                            'name': product_line["description"] or '',
                            # 'date_planned': row.TRANSACTION_DATE or False,
                            # 'account_analytic_id': False,
                            'product_uom_qty': product_line["product_qty"] or 0,
                            # 'qty_received_manual': 0,
                            # 'discount': discount or 0,
                            'product_uom': product.uom_id.id or request.env.ref(
                                'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                            'price_unit': product_line["rate"] or 0,
                            'tax_id': tax,
                        }))
            if to_company_detail2:
                sale_order_1 = request.env['sale.order'].sudo().create({
                    'partner_id': to_company_detail2.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
#                     'date_order':row["master"]["date_order"] or False,
#                     'date_planned':row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':from_company_detail.id
                })
#                 request.env.cr.commit()
                if sale_order_1:
                    sale_order_1.action_confirm()
                    if sale_order_1.picking_ids:
                        for picking in sale_order_1.picking_ids:
                            for product_line in row["child"]:
                                product_lot_number = product_line["lot_number"]
                                product = product_line["name"] and request.env['product.product'].sudo().search(
                                    [('name', '=', product_line["name"])], limit=1) or False
                                if product:
                                    for line_ids in picking.move_line_ids:
                                        if product.id == picking.product_id.id and product_line[
                                            "description"] == line_ids.move_id.name:
                                            product_lot_number = product_line["lot_number"]

                                            qty_done = product_line["qty_done"]
                                            lot_no = request.env['stock.production.lot'].sudo().search(
                                                [('company_id', '=', from_company_detail.id),
                                                 ('name', '=', product_lot_number)])
                                            print("LOT")
                                            print(lot_no.name)
                                            line_ids.lot_id = lot_no.id
                                            line_ids.lot_name = lot_no.name
                                            line_ids.qty_done = qty_done
                            picking.button_validate()
                            pick_to_backorder = request.env['stock.immediate.transfer']
                            stock_immediate = pick_to_backorder.sudo().create(
                                {'pick_ids': [(6, 0, sale_order_1.picking_ids.ids)]})
                            request.env.cr.commit()
                so_numbers.append({
                    'soNumber': sale_order_1.name,
                    'orderID': row["master"]["orderID"]
                })
        po_numbers = []
        for row in rec["data"]:
            vendor_gst = row["master"]["partner_id"]["gst_no"]
            purchase_to_company = row["master"]["company_ware_house"]["name"]
            if purchase_to_company == 'JOTHIPURAM':
                purchase_to_company_detail2 = purchase_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if purchase_to_company == 'KAVALANGAD':
                purchase_to_company_detail2 = purchase_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

            purchase_from_company = row["master"]["partner_id"]["name"]
            if purchase_from_company == 'JOTHIPURAM':
                purchase_from_company_detail = purchase_from_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
            if purchase_from_company == 'KAVALANGAD':
                purchase_from_company_detail = purchase_from_company and request.env['res.partner'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
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
                if gst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', purchase_to_company_detail2.id), ('amount', '=', str(gst)), ('type_tax_use', '=', "purchase"),
                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                if igst:
                    tax_variant = request.env['account.tax'].sudo().search(
                        [('company_id', '=', purchase_to_company_detail2.id), ('amount', '=', str(igst)), ('type_tax_use', '=', "purchase"),
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
                            'tracking':'lot',
                            'categ_id': 1,
                            'standard_price': product_line["rate"],

                        }

                        add_product = request.env['product.template'].sudo().create(product_details)
                        request.env.cr.commit()
                        product = product_item and request.env['product.product'].sudo().search(
                        [('name', '=', product_item)], limit=1) or False
                    if product:
                        order_line.append((0, 0, {
                            'display_type': False,
                            # 'sequence': 10,
                            'product_id': product.id,
                            'name': product_line["description"] or '',
                            # 'date_planned': row.TRANSACTION_DATE or False,
                            'account_analytic_id': False,
                            'product_qty': product_line["product_qty"] or 0,
                            'qty_received_manual': 0,
                            # 'discount': discount or 0,
                            'product_uom': product.uom_id.id or request.env.ref(
                                'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                            'price_unit': product_line["rate"] or 0,
                            'taxes_id': tax,
                        }))
            if vendor:
                purchase_order_1 = request.env['purchase.order'].sudo().create({
                    'partner_id': purchase_from_company_detail.id,
                    # 'partner_ref': row.SALES_ORDER_NUMBER or '',
                    # 'origin': row.INVOICE_NUM or '',
                    #                     'date_order':row["master"]["date_order"] or False,
                    #                     'date_planned':row["master"]["date_order"] or False,
                    # 'partner_id': self.env.ref('base.main_partner').id,
                    # 'name': row.INVOICE_NUM or '',
                    'order_line': order_line,
                    'company_id':purchase_to_company_detail2.id
                })
#                 request.env.cr.commit()

                if purchase_order_1:
                    po_numbers.append({
                        'poNumber': purchase_order_1.name,
                        'orderID': row["master"]["orderID"]
                    })
        return po_numbers, so_numbers



class SCAItemMaster(http.Controller):
    @http.route('/data/SCA/ItemMaster', type='json', csrf=False, auth='public')
    def SCAItemMaster(self):
        SCAItemMaster_rec = request.env['product.template'].sudo().search([('categ_id', 'like', "Finished")])
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

    #*************************
