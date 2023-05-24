from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class QualityParams(models.Model):
    _name = 'quality.params'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    name = fields.Char("Category Name")
    cid = fields.Char("Quality Check id")
    pdt_ctgs = fields.Many2one("product.category", string="Product Category")
    operation_type = fields.Many2one("stock.picking.type", string="Operation Types")


    qc_params_line_ids = fields.One2many('quality.params.line', 'params_id', string='Params line')

    qc_after_params_ids = fields.One2many('quality.params.after', 'after_params_id', string='After SubC')


    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)

    is_sub = fields.Boolean("Is Subcontract")




    class QualityParamsLiness(models.Model):
        _name = "quality.params.line"

        sno = fields.Integer(string='Sno')
        questions = fields.Char( string='Questions')
        res = fields.Char(string='Response')
        remark = fields.Char(string="Remark")

        params_id = fields.Many2one('quality.params', string='Params')


    class QualityParamsAfter(models.Model):
        _name = "quality.params.after"

        sn = fields.Integer(string='Sno')
        af_qs = fields.Char(string='Questions')
        af_res = fields.Char(string='Response')
        af_remark = fields.Char(string="Remark")

        after_params_id = fields.Many2one('quality.params', string='Params')

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('quality.params') or _('New')
        res = super(QualityParams, self).create(vals)
        return res