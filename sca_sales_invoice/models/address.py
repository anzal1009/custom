from odoo import models, fields, api


class AccountMoveDepo(models.Model):
    _inherit = 'account.move'

    depo_address = fields.Many2one("stock.location", string="Depo Name")



class SaleOrderAddress(models.Model):
    _inherit = 'sale.order'

    depo_address = fields.Many2one("stock.location", string="Depo Name")






class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        if self.depo_address:
            invoice_vals['depo_address'] = self.depo_address.id
        return invoice_vals


