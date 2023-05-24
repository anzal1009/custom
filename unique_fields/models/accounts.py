from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CoaUnique(models.Model):
    _inherit = 'account.account'

    refe = fields.Char(string="Ref",compute='_compute_name',readonly=0)

    _sql_constraints = [
        ('code_company_refe', 'unique (refe,company_id)', 'The Ref of the account must be unique per company !'),
        ('code_company_name', 'unique (name,company_id)', 'The Name of the account must be unique per company !')
    ]

    # @api.constrains('name')
    # def duplicate_name(self):
    #     for rec in self:
    #         name = self.env['account.account'].sudo().search([('name','=',self.name)])
    #         if name:
    #             raise ValidationError("The Name of the account must be unique per company !")

    @api.depends('name')
    def _compute_name(self):
        for rec in self:
            if rec.name:
                rec.refe = rec.name
            else:
                rec.refe = None


