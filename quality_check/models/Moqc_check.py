from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class MoqcCheck(models.Model):
    _name = 'moqc.check'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    name = fields.Char("Name"  )
    tid = fields.Char("Transfer No")
    poid = fields.Char("MO No")
    product_id =  fields.Many2one("product.product",string="Product")
    qdate= fields.Date("Date" ,required=True)
    user = fields.Many2one('res.users', 'Created User', required=True, index=True,
                                 default=lambda self: self.env.user)
    bld_sheet = fields.Char("Blend Sheet No" )
    source_loc_id = fields.Many2one("stock.location", string="Source Location")
    dest_loc_id = fields.Many2one("stock.location", string="Destination Location")

    responsible = fields.Many2one('res.users', 'Resp User', related="dest_loc_id.qc_representative")


    state = fields.Selection(
        [('d', 'Draft'), ('o', 'Ongoing'), ('c', 'Completed')],
        default='d', string='Status', tracking=True)


    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)

    pdt_ctg = fields.Char( "Product Category")

    lot_id = fields.Many2one("stock.production.lot",string="Lot number")

    pdt_ctg_id = fields.Many2one("product.category",string="Product Categories")
    pdt_temp_ids = fields.Many2many('params.moqc', "qc_mo_pdt_tmp", "qc_mo_ids", "pdt_mo_tmp_id",
                                    string="Category Templates")

    moqc_line_idss = fields.One2many('moqc.liness', 'moqc_ids', string='QC line')

    moqc_lines_idss = fields.One2many('moqc.liness.line', 'moqc_idss', string='PM line')

    pdt_temp = fields.Many2one('params.moqc',"Category Templates")

    failure = fields.Boolean("QC Faliures", compute='_compute_failure')

    failure_count =fields.Integer(string="Failure count" ,compute='_compute_failure_count')

    tag = fields.Selection([('pd', 'Pending'), ('pas', 'Passed'), ('fa', 'Failed')], string='Tags',
                           compute='_compute_tags', default='pd')
    tags = fields.Selection([('pds', 'Pending'), ('pa', 'Passed'), ('fai', 'Failed')], string='Tags', default='pds')

    def _compute_tags(self):
        mo = self.env['mrp.production'].search([('name', '=', self.poid)], limit=1) or False
        for t in self:
            if t.failure == True:
                t.tag = 'fa'
                t.tags= 'fai'
                mo.tagss ='fai'

            elif t.failure == False:
                t.tag = 'pas'
                t.tags = 'pa'
                mo.tagss = 'pa'
            else:
                t.tag ='pd'
                t.tags ='pds'
                mo.tagss ='pds'



    def _compute_failure_count(self):
        for rec in self:
            if rec.moqc_line_idss:
                for re in rec.moqc_line_idss:
                    if re:
                        # print(re)
                        failed_count = self.env['moqc.liness'].search_count(
                            [("moqc_ids", '=', self.id), ('ress', '=', 'F')])
                        if failed_count:
                            rec.failure_count = failed_count
                        else:
                            rec.failure_count = 0
                    else:
                        rec.failure_count = 0
            else:
                rec.failure_count = 0



    @api.depends('failure_count')
    def _compute_failure(self):
        for recc in self:
            if recc.failure_count > 0:
                recc.failure = True
            else:
                recc.failure = False





    @api.onchange('pdt_temp_ids')
    def _onchange_pdt_temp_ids(self):
        for rec in self:
            if rec.pdt_temp_ids:
                lines = [(5, 0, 0)]
                # lines = []
                print("self.pdt_temp", self.pdt_temp_ids.moqc_params_line_ids)
                for line in self.pdt_temp_ids.moqc_params_line_ids:
                    val = {
                        'questionss': line.questions,

                    }
                    lines.append((0, 0, val))
                rec.moqc_line_idss = lines

    class QualityLiness(models.Model):
        _name = "moqc.liness"


        questionss = fields.Char(string='Questions')
        # product = fields.Many2one('product.template', string="Products")
        ress = fields.Selection(
        [('p', 'Pass'), ('F', 'Fail')],
         string='Response',tracking=True)
        remarks = fields.Char(string="Remark",tracking=True)

        moqc_ids = fields.Many2one('moqc.check', string='Quality')



    ####### NOT NEEDED ######

    class MoqcLiness(models.Model):
        _name = "moqc.liness.line"

        questionss = fields.Char(string='Questions')
        ress = fields.Char(string='Response',tracking=True)
        no = fields.Char(string='False',tracking=True)
        remarks = fields.Char(string="Remark",tracking=True)

        moqc_idss = fields.Many2one('moqc.check', string='Quality')



    def action_ongoing(self):
        self.state = 'o'

    def action_done(self):
        mo = self.env['mrp.production'].search([('name', '=', self.poid)], limit=1) or False
        # print(mo.name)
        self.state = 'c'
        # mo.state ='confirmed'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('moqc.check') or _('New')
        res = super(MoqcCheck, self).create(vals)
        return res