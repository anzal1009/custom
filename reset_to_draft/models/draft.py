from odoo import models


class VendorBillDraft(models.Model):
    _inherit = "account.move"

    def action_reset_draft(self):
        for row in self:
            VendorBillNumber = self.name
            VendorBill = self.env['account.move'].sudo().search([('name', '=', VendorBillNumber)]) or False
            for rec in VendorBill:
                rec.state = "draft"
                # rec.name = ""
