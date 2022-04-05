from odoo import api, models, fields


class CreateInvoiceWizard(models.TransientModel):
    _name = "create.invoice.wizard"

    name = fields.Many2one('medical.staff', string='Sales Person')
    cname = fields.Char(string="Customer Name")
    product = fields.Text(string='Product')


    def action_create(self):
        vals = {
            'name': self.name.id,
            'cname': self.cname,
            'product':self.product,
        }

        new_appointment = self.env['medical.sales'].create(vals)

