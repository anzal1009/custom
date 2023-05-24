from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class Journal1(http.Controller):
    @http.route('/journal/entry', type='json', auth='user')

    def action_done(self):
        for rec in self:
            debit = credit = rec.currency_id.compute(rec.paid_amount, rec.currency_id)
            if rec.state == 'draft':
                raise UserError(
                    _("Only a Submitted payment can be posted. Trying to post a payment in state %s.") % rec.state)

            sequence_code = 'hr.advance.sequence'
            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(
                sequence_code)

            move = {
                'name': '/',
                'journal_id': rec.journal_id.id,
                'date': rec.payment_date,

                'line_ids': [(0, 0, {
                    'name': rec.name or '/',
                    'debit': debit,
                    'account_id': rec.advance_account.id,
                    'partner_id': rec.employee_id.user_id.partner_id.id,
                }), (0, 0, {
                    'name': rec.name or '/',
                    'credit': credit,
                    'account_id': rec.journal_id.default_credit_account_id.id,
                    'partner_id': rec.employee_id.user_id.partner_id.id,
                })]
            }
            move_id = self.env['account.move'].create(move)
            move_id.post()
            return rec.write({'state': 'paid', 'move_id': move_id.id})