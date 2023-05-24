from odoo import api, models, fields, _
from odoo.exceptions import UserError



class MoCostButton(models.TransientModel):
    _name = "mo.cost.wizard"

    products = fields.Char("Product")
    mo_wiz_line_ids = fields.One2many('mo.cost.lines', 'mo_wiz_ids', string='Mo line')


class MoCostLines(models.TransientModel):
    _name = "mo.cost.lines"

    product = fields.Char(string='Product')
    qty = fields.Char(string='Quantity')
    lot = fields.Char(string="Lot Numbers")
    price =fields.Char("Price")
    lot_qty =fields.Char("Lot Quantity")

    mo_wiz_ids = fields.Many2one('mo.cost.wizard', string='Cost')