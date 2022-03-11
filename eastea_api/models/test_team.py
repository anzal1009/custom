from odoo import models, fields


class QualityCheck(models.Model):
    _name = "quality.team"

    name = fields.Char(string='Team Name')
    email = fields.Char(string='Email id')
    comp = fields.Many2one('res.company',string="Company")
    emp = fields.Many2many('res.partner',string="Employees")