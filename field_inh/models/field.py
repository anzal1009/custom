from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class StockMoveInheritField(models.Model):
    _inherit = 'stock.move.line'

    qtys = fields.Char('Quantity')
