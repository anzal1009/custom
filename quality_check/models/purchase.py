from odoo import models, fields, api, _, tools


class PurchaseLot(models.Model):
    _inherit = "stock.move"

    ch = fields.Char(string="fil")

    def def_confirm(self):
        print("yess")