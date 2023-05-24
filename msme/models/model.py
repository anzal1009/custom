from odoo import models, fields, api, _
from odoo.exceptions import ValidationError





class ResMsmeUpdate(models.Model):
    _inherit = 'res.partner'

    msme = fields.Boolean("Is a MSME")

    @api.onchange('msme')
    def onchange_msme(self):
        if self.msme == True:
            days =  self.env['account.payment.term'].search([('name', '=', "45 Days")])
            self.property_supplier_payment_term_id = days.id

        else:
            self.property_supplier_payment_term_id = None
