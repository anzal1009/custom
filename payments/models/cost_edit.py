from odoo import fields, models, tools

class CostEdit(models.Model):
    _inherit = 'stock.valuation.layer'

    value = fields.Monetary('Total Value', readonly=0)
    unit_cost = fields.Monetary('Unit Value',readonly=0,)


