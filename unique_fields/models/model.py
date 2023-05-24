from odoo import models, fields, api
from odoo.exceptions import ValidationError




class AccountUnique(models.Model):
    _inherit = 'account.analytic.account'

    status = fields.Selection([('p', 'Pending'), ('s', 'Saved')], string='Status', default='p')



    # @api.model
    # def create(self, vals):
    #
    #
    #     print("yesss")
    #     # for i in self:
    #     self.status = "s"
    #     res = super(AccountUnique, self).create(vals)
    #     return res



    @api.constrains('name')
    def duplicate_name(self):
        for rec in self:
            name = self.env['account.analytic.account'].sudo().search([('name','=',self.name)])
            print(self.name)
            for i in name:
                print(i.active)
            if name:
                raise ValidationError("The Name of the account must be unique per company !")


    #
    # _sql_constraints = [
    #     ('unique_name', 'unique (name)', 'This Analytic Account already exists'),
    #     ('unique_code', 'unique (code)', 'This Analytic Account Code already exists')
    # ]

