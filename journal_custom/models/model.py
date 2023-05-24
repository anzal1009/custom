from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class JournalNewFields(models.Model):
    _inherit = "account.move"

    j_value = fields.Float(compute='_compute_jornal_total',string="Journal Total",store=True)


    @api.constrains('j_value')
    def _check_total_journl(self):
        for record in self:
            if record.move_type=='entry':
                if not record.statement_line_id:
                    if record.j_value != 0:
                        raise ValidationError(_('Cannot create unbalanced journal entries, Differences debit - credit: "%s"') % (record.j_value))

                # raise ValidationError("Cannot create unbalanced journal entries")

    @api.depends('line_ids')
    def _compute_jornal_total(self):
        for line in self:
            total_credit = 0
            total_debit = 0
            for amount in line.line_ids:
                # print(amount.credit)
                total_credit =total_credit + amount.credit
                total_debit = total_debit + amount.debit
                # print("credit", total_credit)
                # print("debit", total_debit)

            line.j_value =total_debit  - total_credit





