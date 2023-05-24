from odoo import models, fields, api
from odoo.http import request


class AccountMoveDepo(models.Model):
    _inherit = 'account.move'

    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse")











class SaleOrder(models.Model):
    _inherit = "sale.order"

    wareh = fields.Many2one("stock.warehouse", string="Wh2")

    warehouse_id = fields.Many2one("stock.warehouse", readonly=True,string="Warehouse",
           states={'draft': [('readonly', True)],'sale': [('readonly', True)],'cancel': [('readonly', True)], 'done': [('readonly', True)]})



    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id:
            for rec in self:
                warehouse = request.env['stock.warehouse'].sudo().search([('name','=',self.user_id.warehouse.name)])
                if warehouse:
                    rec.wareh = warehouse.id

    @api.onchange('wareh')
    def onchange_wareh_id(self):
        if self.wareh:
            for rec in self:
                rec.warehouse_id = rec.wareh





    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        if self.warehouse_id:
            invoice_vals['warehouse_id'] = self.warehouse_id.id
        return invoice_vals




