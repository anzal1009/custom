from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger



class SaleAddonInvoice(models.Model):
    _inherit = 'sale.order'

    value = fields.Float(string='Additional Value')

    def action_change(self):
        print("yes")
        sales = self.env['sale.order'].sudo().search([])
        for val in self.order_line:
            value = self.value
            val.extra = value
            if val.extra and val.sum == 0:
                val.sum = val.price_unit
            val.price_unit = (float(val.sum) + float(val.extra))




class PurchaseAddonInvoice(models.Model):
    _inherit = 'purchase.order'

    values = fields.Float(string='Additional Value')

    def action_addition(self):
        print("yes")
        sales = self.env['purchase.order'].sudo().search([])
        for val in self.order_line:
            value = self.values
            val.extra = value
            if val.extra and val.sum == 0:
                val.sum = val.price_unit
            val.price_unit = (float(val.sum) + float(val.extra))



