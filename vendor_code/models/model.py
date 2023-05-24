from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code = fields.Char("Code", readonly=True, store=True, force_save="1")

    @api.onchange('supplier', 'customer')
    def set_partner_code(self):
        for record in self:
            if record.supplier is True:
                record.code = self.env['ir.sequence'].next_by_code('vendor.code')
            if record.customer is True:
                record.code = self.env['ir.sequence'].next_by_code('customer.code')
            if record.supplier is True and record.customer is True:
                record.code = self.env['ir.sequence'].next_by_code('vendor.customer.code')
