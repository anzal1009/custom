from odoo import models, fields, api


class BankInherited(models.Model):
    _inherit = "res.partner.bank"

    ifsc = fields.Char("IFSC Code")



class VendorBankInherited(models.Model):
    _inherit = "res.partner"

    ifsc = fields.Char("IFSC Code")