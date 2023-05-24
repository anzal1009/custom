from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class SaleInvoice(models.Model):
    _inherit = 'purchase.order.line'

    extra = fields.Char(string='Additional Charges',tracking=True)
    sum = fields.Float(string="Sum off")

    @api.onchange('extra')
    def onchange_compute_extra(self):
        if self.extra and self.sum == 0:
            self.sum = self.price_unit
        # if self.extra == 0:
        #     self.sum = 0.00
        self.price_unit = (float(self.sum) + float(self.extra))



