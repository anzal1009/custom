from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PaymentInherit(models.Model):
    _inherit = "account.payment"

    coa = fields.Many2one("account.account",string="Account")
    analytical = fields.Many2one("account.analytic.account",string="Analytical Account")


    def action_post(self):
        if self.partner_id:
            res = super().action_post()
            return res


        else:
            for rec in self:
                rec.button_open_journal_entry()
                for l in rec.move_id.line_ids:
                    l.analytic_account_id = self.analytical

                # journal_entry = self.env['account.move'].sudo().create({
                #     'move_type': "entry",
                #     'ref': "ref",
                #     'date': self.date,
                #     'journal_id': self.journal_id.id,
                #     'company_id': self.company_id.id,
                #     'line_ids': [(0, 0, {
                #         'name': "ref",
                #         'debit': self.amount,
                #         'account_id':self.coa.id,
                #         'analytic_account_id':self.analytical.id
                #
                #     }), (0, 0, {
                #         'name': "ref",
                #         'credit': self.amount,
                #         'account_id': 74 ,
                #         'analytic_account_id': self.analytical.id
                #
                #     })]
                # })
                #
                # self.move_id = journal_entry.id



                # l.line_ids[1].account_id = self.coa
                # l.line_ids[0].account_id = self.journal_id.default_account_id

                #
                if l.debit:

                    print(l.account_id.name)
                    # l.account_id = self.coa.id

                    # if l.credit:
                    #     l.account_id = self.journal_id.default_account_id


                    res = super().action_post()
                    return res


                        # print("yesss")

