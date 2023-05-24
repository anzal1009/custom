# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", domain="[('company_id','=',company_id)]",
                                   readonly=True, states={'draft': [('readonly', False)]})

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.move_type == 'out_invoice':
                if move.id and not move.warehouse_id:
                    raise UserError(_("Please select warehouse"))
                if move.id and not move.warehouse_id.sequence_id:
                    raise UserError(_("Please assign sequence to %s", move.warehouse_id))
                if not move.name or move.name == '/':
                    move.name = move.warehouse_id.sequence_id._next() if move.warehouse_id else '/'
            else:
              return super(AccountMove, self)._compute_name()


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    sequence_id = fields.Many2one('ir.sequence', string="Sequence for Invoice",
                                  domain="[('company_id','=',company_id)]")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()

        if self.warehouse_id:
            invoice_vals['warehouse_id'] = self.warehouse_id.id
        return invoice_vals


