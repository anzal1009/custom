from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class ParamsMoqc(models.Model):
    _name = 'params.moqc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    name = fields.Char("Category Name")
    cid = fields.Char("Quality Check id")
    pdt_ctgrs = fields.Many2one("product.category", string="Product Category")

    operation_types = fields.Many2one("stock.picking.type", string="Operation Types")

    moqc_params_line_ids = fields.One2many('moqc.params.line', 'moqc_params_id', string='Params line')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)


    class MoqcParamsLiness(models.Model):
        _name = "moqc.params.line"

        questions = fields.Char( string='Questions')
        res = fields.Char(string='Response')
        remark = fields.Char(string="Remark")


        moqc_params_id = fields.Many2one('params.moqc', string='Params')

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('params.moqc') or _('New')
        res = super(ParamsMoqc, self).create(vals)
        return res