from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger



class StockMoveLineIrnInherit(models.Model):
    _inherit = 'stock.move'

    rice = fields.Float("Price", store=True, force_save="1", tracking=True)
    taxes_id = fields.Many2one("account.tax", "Taxes")
    sub_totals = fields.Char("Subtotal")