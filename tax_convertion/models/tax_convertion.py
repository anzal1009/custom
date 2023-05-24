from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ImportPickings(models.TransientModel):
    _name = "import.purchase.order"

# class PurchaseTax(models.Model):
#     _inherit = 'purchase.order'

    def action_convert(self):
        print("ooo")
    #
    #     purchase_orders = self.env['purchase.order'].sudo().search([()]) or False
    #     print(purchase_orders.id)