from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritLot(models.Model):
    _inherit = 'stock.quant'

    lot_costs = fields.Float(compute='_compute_lot_unit_cost',string="Lot Unit Cost")
    total_lot_cost = fields.Float(string="Total Cost")


    # def _compute_lot_unit_cost(self):
    #     for rec in self:
    #         lot_cost = self.env['stock.production.lot'].sudo().search(
    #                             [('name', '=',self.lot_id.name),('company_id', '=', self.company_id.id)]) or False
    #         print(lot_cost)
    #         # print(lot_cost)
    #         for i in lot_cost:
    #             # if lot_cost:
    #             rec.lot_costs = i.lot_cost
    #             # else:
    #             #     rec.lot_costs = 0.00
