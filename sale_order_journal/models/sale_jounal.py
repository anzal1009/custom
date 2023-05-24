from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger




class SaleInvoice(models.Model):
    _inherit = 'account.move'

    acc = fields.Many2one('account.account',string='Account')
    analytic = fields.Many2one('account.analytic.account',string="Analytic Accounts")


    def action_journal(self):
        sales = self.env['account.move'].sudo().search([])

        for jo in self.invoice_line_ids:
            account_name=self.acc

            jo.account_id = account_name.id


    def action_analytic(self):
        sales = self.env['account.move'].sudo().search([])

        for jo in self.invoice_line_ids:
            anlytic_name = self.analytic

            jo.analytic_account_id = anlytic_name.id




