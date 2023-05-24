from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveSequence(models.Model):
    _inherit = 'account.move'


    extra_name = fields.Char(string='Sequence Name')
    # name = fields.Char(string='Name',readonly=0)


    #
    # @api.onchange('account_id', 'journal_id')
    # def _on_change_account_id(self):

    @api.depends('state', 'journal_id', 'date')
    def _compute_name(self):
        if self.journal_id.name == "Tax Invoices":
            print('yess')
        else:
            print("nooo")

    #
    # def action_sequence_name(self):
    #
    #     if self.extra_name:
    #         name = self.extra_name
    #         number = self.sequence_number
    #         # journal = self.env['account.move'].sudo().search(['name','=',name])
    #         # if journal:
    #         #     journal.name =name
    #         self.sequence_prefix = name
    #         self.name = name + str(number)
