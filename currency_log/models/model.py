from odoo import models, fields, api
from odoo.exceptions import ValidationError





class CurrencyInherited(models.Model):

    _name = 'res.currency'
    _inherit = ['res.currency','mail.thread','res.currency.rate']


    inverse_company_rate = fields.Float(tracking=True )

    new_rates = fields.Float("rate",tracking=True,readonly=True)


    @api.onchange('rate_ids')
    def _onchange_inverse_rate(self):
        for rec in self:
            rates = []
            for lines in rec.rate_ids:
                rates.append(lines.inverse_company_rate)
                rec.new_rates = rates[0]












class CurrencyRateInherited(models.Model):

    _inherit = ['res.currency.rate']



    new_rate = fields.Float(string='New Rate',tracking=True)





