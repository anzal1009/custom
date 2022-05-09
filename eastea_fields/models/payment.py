from odoo import models, fields, api



class ManufactureOrder(models.Model):
    _inherit = 'account.payment'

    pay_ref = fields.Char("Payment Refernce")
