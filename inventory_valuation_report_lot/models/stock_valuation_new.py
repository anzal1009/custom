from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockLotValue(models.Model):
    _name = 'stock.lot.value'

    date = fields.Date("Date")
    product_id = fields.Many2one('product.product', 'Product',  required=True, auto_join=True)
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id')
    quantity = fields.Float('Quantity', help='Quantity', readonly=True, digits='Product Unit of Measure')
    uom_id = fields.Many2one(related='product_id.uom_id', readonly=True, required=True)
    unit_cost = fields.Float('Unit Value', readonly=True)
    value = fields.Float('Total Value', readonly=True)