from odoo import models, fields, api



class ManufactureOrder(models.Model):
    _inherit = 'mrp.production'

    blend = fields.Char("Blend Sheet No")
    categ =fields.Many2one(related='product_id.categ_id')