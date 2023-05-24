from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class QualityFail(models.Model):
    _name = 'quality.fail'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    name = fields.Char("Category Name")
    fid = fields.Char("Reference")
    fdate= fields.Date("Date")
    user = fields.Many2one('res.users',"User")
    source = fields.Char("Source Document")

    qc_fail_line_ids = fields.One2many('quality.fail.line', 'fail_id', string='Fail line')

    # poid = fields.Char("PO No")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)




    class QualityFailLines(models.Model):
        _name = "quality.fail.line"

        sno = fields.Integer(string='Sno')
        product = fields.Char( string='Product')
        res = fields.Char(string='Response')
        remark = fields.Char(string="Remark")

        fail_id = fields.Many2one('quality.fail', string='fail')


    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('quality.fail') or _('New')
        res = super(QualityFail, self).create(vals)
        return res

