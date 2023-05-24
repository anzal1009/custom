from odoo import models, fields, api, _, tools


class SalesDiscount(models.Model):
    _inherit = "sale.order.line"


    disc = fields.Float("Discount")

    @api.onchange('disc')
    def onchange_disc(self):
        print("onchange")
        for line in self:
            line.price_subtotal = line.price_subtotal - line.disc