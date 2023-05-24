from odoo import models, fields, api


class UserWarehouse(models.Model):
    _inherit = 'res.users'

    warehouse = fields.Many2one("stock.warehouse", string="Warehouse")