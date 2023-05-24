from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    # res = fields.Many2one('stock.move.line',string='res')
    lot = fields.Many2one('stock.production.lot',string='LOT No',domain="[('product_id','=',product_id)]")
    # lot = fields.Many2one(relation='production_id.lot_id.id',string='LOT No',domain="[('product_id','=',product_id)]")



    @api.onchange('lot')
    def onchange_lot(self):
        if self.lot:
            for k in self:
                # print(k)
                for l in k.move_line_ids:
                    l.update({
                                    'lot_id': k.lot,
                                })
                    # l.lot_id = k.lot

