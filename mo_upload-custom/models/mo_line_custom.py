from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class SaleInvoice(models.Model):
    _inherit = 'purchase.order.line'

    extra = fields.Char(string='Additional Charges')