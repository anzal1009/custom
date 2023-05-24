from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InventoryAging(models.Model):
    _name = 'inventory.age'

    date = fields.Date("Date")
    product_id = fields.Char('Products', auto_join=True)
    quantity = fields.Float('Quantity', help='Quantity',  digits='Product Unit of Measure')
    uom_id = fields.Char("UOM")