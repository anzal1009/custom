# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection([('domestic', 'Domestic'), ('exp/imp', 'Export/Import'),
                                     ('customer/supplier', 'Customer/Supplier')], string='Type of Partner')

    @api.onchange('partner_type', 'supplier', 'customer')
    def set_partner_ref(self):
        for record in self:
            if not record.ref:
                if record.partner_type == 'domestic' and record.supplier is True:
                    record.ref = self.env['ir.sequence'].next_by_code('domestic.vendor.code')
                if record.partner_type == 'domestic' and record.customer is True:
                    record.ref = self.env['ir.sequence'].next_by_code('domestic.customer.code')
                if record.partner_type == 'exp/imp' and record.supplier is True:
                    record.ref = self.env['ir.sequence'].next_by_code('export.import.vendor.code')
                if record.partner_type == 'exp/imp' and record.customer is True:
                    record.ref = self.env['ir.sequence'].next_by_code('export.import.customer.code')
                if record.partner_type == 'customer/supplier' and (record.supplier or record.customer):
                    record.ref = self.env['ir.sequence'].next_by_code('vendor.customer.code')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_code = fields.Char(string="Vendor Code")

    @api.onchange('partner_id')
    def _onchange_purchase_partner(self):
        for i in self:
            if i.partner_id:
                i.vendor_code = i.partner_id.ref

    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        if self.vendor_code:
            invoice_vals['partner_code'] = self.vendor_code
        return invoice_vals


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_code = fields.Char(string="Customer Code")

    @api.onchange('partner_id')
    def _onchange_sale_partner(self):
        for i in self:
            if i.partner_id:
                i.customer_code = i.partner_id.ref

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.customer_code:
            invoice_vals['partner_code'] = self.customer_code
        return invoice_vals


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_code = fields.Char(string="Partner Code")

    @api.onchange('partner_id')
    def _onchange_account_partner(self):
        for i in self:
            if i.partner_id:
                i.partner_code = i.partner_id.ref

    @api.onchange("purchase_vendor_bill_id", "purchase_id")
    def _onchange_purchase_auto_complete(self):

        purchase_id = self.purchase_id
        if self.purchase_vendor_bill_id.purchase_order_id:
            purchase_id = self.purchase_vendor_bill_id.purchase_order_id
        if purchase_id and purchase_id.vendor_code:
            self.partner_code = purchase_id.vendor_code
        return super(AccountMove,self)._onchange_purchase_auto_complete()
