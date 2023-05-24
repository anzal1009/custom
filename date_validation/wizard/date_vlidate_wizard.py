from odoo import api, models, fields, _
from datetime import datetime
from odoo.exceptions import UserError
from odoo import modules




class SaleOrder(models.Model):
    _inherit = 'stock.picking'

    date_done = fields.Datetime(store=True)



    def date_confirm_button(self):
        print("yess")
        # 'confirmation_date' == self.scheduled_date
        action = self.env["ir.actions.actions"]._for_xml_id('date_validation.action_date_validate')
        action['context'] = {'default_sale_id': self.id}
        return action




class DateValidation(models.TransientModel):
    _name = "date.validation.wizard"

    confirmation_date = fields.Datetime('Confirmation Date')
    sale_id = fields.Many2one(
        'stock.picking', string='Transfer Id', readonly=True)

    @api.model
    def _prepare_default_get(self, order):
        default = {
            'sale_id': order.id,
            'confirmation_date': order.date_done,

        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(DateValidation, self).default_get(fields)
        assert self._context.get('active_model') == 'stock.picking', \
            'active_model should be stock.picking'
        order = self.env['stock.picking'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(order)
        res.update(default)
        return res

    def _prepare_update_so(self):
        self.ensure_one()
        return {
            'date_done': self.confirmation_date,
        }

    def action_confirm(self):
    #     super(DateValidation, self).action_confirm()
    #     self.confirmation_date = self.date_done

        self.ensure_one()
        # confirm sale order
        self.sale_id.button_validate()
        vals = self._prepare_update_so()
        self.sale_id.write(vals)
        return True



    # def action_confirm(self):
    #     return {
    #         'date_done': self.confirmation_date,
    #     }
    #     self.button_validate()




