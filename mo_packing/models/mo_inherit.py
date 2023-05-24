from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger

class MrpPacking(models.Model):
    _inherit = 'mrp.production'

    def action_packing(self):
        vals = {
            'name': self.product_id.name,
            'qty': self.product_qty,
            'lot': self.lot_producing_id.name
        }

        new_package = self.env['mrp.packing'].create(vals)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mrp.packing',
                'res_id': new_package.id,
                'context': context
                }
