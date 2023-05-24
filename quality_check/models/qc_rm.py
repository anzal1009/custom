from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class QualityRm(models.Model):
    _name = 'quality.rm'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    name = fields.Char("Name")
    tid = fields.Char("Transfer No")
    poid = fields.Char("PO No")
    qdate= fields.Date("Date")
    state = fields.Selection(
        [('d', 'Draft'), ('o', 'Ongoing'), ('c', 'Completed')],
        default='d', string='Status', tracking=True)

    qc_line_ids = fields.One2many('quality.line', 'qc_id', string='QC line')


    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)

    pdt_ctg = fields.Many2one('product.category', "Product Category")

    # @api.onchange('pdt_ctg')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         if rec.product_id:
    #             lines = [(5, 0, 0)]
    #             # lines = []
    #             print("self.product_id", self.product_id.product_variant_ids)
    #             for line in self.product_id.product_variant_ids:
    #                 val = {
    #                     'product_id': line.id,
    #                     'product_qty': 15
    #                 }
    #                 lines.append((0, 0, val))
    #             rec.appointment_lines = lines



    class QualityLiness(models.Model):
        _name = "quality.line"

        sno = fields.Integer(string='Sno')
        questions = fields.Char( string='Questions')
        res = fields.Char(string='Response')
        remark = fields.Char(string="Remark")

        qc_id = fields.Many2one('quality.rm', string='Quality')










    def action_ongoing(self):
        self.state = 'o'

    def action_done(self):
        self.state = 'c'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('quality.rm') or _('New')
        res = super(QualityRm, self).create(vals)
        return res