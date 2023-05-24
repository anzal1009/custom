
from odoo import api, fields, models, tools, _


class AccountLineINRCur(models.Model):
    _inherit = "account.move.line"

    cost_in_inr_cur = fields.Char(string='Cost In INR', default=0.0)


    # @api.depends('price_unit')
    # def _compute_cost_in_inr_cur(self):
    #     for line in self:
    #         cost_in_inr_cur = line.credit
    #         line.cost_in_inr_cur = cost_in_inr_cur
