from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time






class ExpenseBillAddon(http.Controller):
    @http.route('/data/expensebill_addon', type='json', csrf=False, auth='public')
    def ExpenseAddon(self, **rec):
        for row in rec["data"]:
            bill = row["bill_number"]
            reference = row["ref"]
            analytical = row["analytical"]
            tbref = row["tbref"]

            bill_number = bill and request.env['account.move'].sudo().search(
                [('name', '=', bill)], limit=1) or False
            # print(bill_number.company_id)

            analytical_id = analytical and request.env['account.analytic.account'].sudo().search(
                [('name', '=', analytical),('company_id', '=', bill_number.company_id.id)], limit=1) or False
            # print(analytical_id.id)
            for r in bill_number:
                r.ref = reference
                r.ctnoteno =tbref
                for a in r.invoice_line_ids:
                    a.analytic_account_id = analytical_id.id



