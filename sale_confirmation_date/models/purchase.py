from odoo import models, fields, api,_
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    confirmation_date = fields.Datetime(string="Confirmation Date",store=True)

    def sale_confirm_wizard_button(self):
        """This method is designed to be inherited.
        For example, inherit it if you don't want to start the wizard in
        some scenarios"""
        action = self.env["ir.actions.actions"]._for_xml_id('sale_confirmation_date.update_confirmation_date_action')
        action['context'] = {'default_sale_id': self.id}

        # action = self.env.ref(
        #     'sale_confirmation_date.update_confirmation_date_action').read()[0]
        return action


class confirmationState(models.TransientModel):
    _name = 'confirmation.date'

    confirmation_date = fields.Datetime(string="Confirmation Date",store=True)

    sale_id = fields.Many2one(
        'purchase.order', string='Purchase Order', readonly=True)


    @api.model
    def _prepare_default_get(self, order):
        default = {
            'sale_id': order.id,
            'confirmation_date': order.date_order,

        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(confirmationState, self).default_get(fields)
        assert self._context.get('active_model') == 'purchase.order', \
            'active_model should be purchase.order'
        order = self.env['purchase.order'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(order)
        res.update(default)
        return res

    def _prepare_update_so(self):
        self.ensure_one()
        return {
            'date_order': self.confirmation_date,
        }

    def confirm(self):
        self.ensure_one()
        # confirm sale order
        self.sale_id.action_confirm()
        vals = self._prepare_update_so()
        self.sale_id.write(vals)
        return True