from odoo import models, fields, api



class ManufactureOrder(models.Model):
    _inherit = 'res.partner'

    pan = fields.Char("Pan Number")

    _sql_constraints = [
        ('unique_pan', 'unique (pan)', 'This Pan already exists')
    ]
