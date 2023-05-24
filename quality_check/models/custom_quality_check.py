from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger


class LocationOnline(models.Model):
    _inherit = 'stock.location'

    is_online = fields.Boolean("Is Online Sale")
    qc_representative = fields.Many2one('res.users',"Q\C Incharge")




class CustomQualityCheck(models.Model):
    _name = 'custom.quality.check'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    # @api.model
    # def default_get(self, fields):
    #     # if self.pdt_temp_ids
    #     print(self.pdt_temp_ids.ids)
    #     res = super(QualityCheck, self).default_get(fields)
    #     return res



    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    name = fields.Char("Name" )
    tid = fields.Char("Transfer No")
    poid = fields.Char("PO No")
    qdate= fields.Date("Date" ,required=True)
    user = fields.Many2one('res.users', 'Created User', required=True, index=True,
                                 default=lambda self: self.env.user)
    resp_user =fields.Many2one('res.users', 'Responsible User',readonly=True)

    state = fields.Selection(
        [('d', 'Draft'), ('o', 'Ongoing'), ('c', 'Completed')],
        default='d', string='Status', tracking=True)

    op_type = fields.Many2one("stock.picking.type",string="Operation")


    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)

    pdt_ctg = fields.Many2one("product.category",string="Product Category")
    pdt_ctg_ids = fields.Many2many("product.category","qc_check_pdt_ctg","qc_id","pdt_ctg_id",  string="Product Categories")

    qc_line_idss = fields.One2many('quality.liness', 'qc_ids', string='QC line')
    is_online_sale = fields.Boolean("Online Sale")

    after_qc_line_ids = fields.One2many('after.qc.lines', 'a_qc_ids', string='QC Subcontracting line')

    qc_prdt_line_ids = fields.One2many('product.quality.lines', 'qc_p_ids', string='Product QC lines')

    pdt_temp = fields.Many2one('quality.params',"Category Templates 0")

    pdt_temp_ids = fields.Many2many('quality.params',"qc_check_pdt_tmp","qc_ids","pdt_tmp_id",string="Category Templates")
    #
    failures = fields.Boolean("POQC Faliures" ,compute='_compute_op_fail',default=False)
    pdt_fail = fields.Boolean("Product Faliures" ,compute='_compute_pdt_fail',default=False)

    state_hide = fields.Boolean("State Hide")
    show_after = fields.Boolean("Show line")
    notes = fields.Text("Notes")

    tag = fields.Selection([('pd', 'Pending'),('pas', 'Passed'),('fa', 'Failed')],string='Tags',compute='_compute_tag',default='pd')
    tags = fields.Selection([('pds', 'Pending'),('pa', 'Passed'),('fai', 'Failed')],string='Tags',default='pds')

    fail_count = fields.Integer(string="Fail count" ,compute='_compute_fail_count')
    op_fail_count = fields.Integer(string="Operation count" ,compute='_compute_op_fail_count')
    source_loc_id = fields.Many2one("stock.location",string="Source Location")
    dest_loc_id = fields.Many2one("stock.location",string="Destination Location")

    @api.constrains('op_type')
    def _check_resp_user(self):
        for rec in self:
            print(rec.op_type.code)
            if rec.op_type.code== "outgoing" or "internal":
                rec.resp_user = rec.source_loc_id.qc_representative.id
            else:
                rec.resp_user = rec.dest_loc_id.qc_representative.id




    @api.constrains('source_loc_id')
    def _check_is_online_sale(self):
        for record in self:
            # print(record.source_loc_id.is_online)
            if record.source_loc_id.is_online == True:
                record.is_online_sale = True
            else:
                record.is_online_sale = False





    def _compute_tag(self):
        transfer = self.env['stock.picking'].search([('name', '=', self.tid)], limit=1) or False
        for m in self:
            if m.failures == True:
                m.tag = 'fa'
                m.tags= 'fai'
                transfer.tagss= 'fai'
            if m.pdt_fail == True:
                m.tag = 'fa'
                m.tags = 'fai'
                transfer.tagss = 'fai'

            elif m.failures == False:
                m.tag = 'pas'
                m.tags = 'pa'
                transfer.tagss = 'pa'
            else:
                m.tag ='pd'
                m.tags ='pds'
                transfer.tagss ='pds'



    #### operation fail
    def _compute_op_fail_count(self):
        for r in self:
            if r.qc_line_idss:
                for recrd_line in r.qc_line_idss:
                    if recrd_line:

                        # r.op_fail_count = 1
                        op_fail_count = self.env['quality.liness'].search_count([("qc_ids",'=',self.id),('ress','=','F')])
                        if op_fail_count:
                            r.op_fail_count = op_fail_count

                        else:
                            r.op_fail_count = 0
                    else:
                        r.op_fail_count = 0
            else:
                r.op_fail_count = 0


    @api.depends('op_fail_count')
    def _compute_op_fail(self):
        for re in self:
            if re.op_fail_count >0 :
                re.failures = True

            else:
                re.failures = False



    #### product Fail

    def _compute_fail_count(self):
        for rec in self:
            if rec.qc_prdt_line_ids:
                for rec_line in rec.qc_prdt_line_ids:
                    if rec_line:
                        print(rec_line)
                        fail_count = self.env['product.quality.lines'].search_count(
                            [("qc_p_ids", '=', self.id), ('p_responce', '=', 'F')])
                        if fail_count:
                            rec.fail_count = fail_count

                        else:
                            rec.fail_count = 0
                    else:
                        rec.fail_count = 0
            else:
                rec.fail_count = 0

    @api.depends('fail_count')
    def _compute_pdt_fail(self):
        for recc in self:
            if recc.fail_count >0:
                recc.pdt_fail=True

            else:
                recc.pdt_fail = False







    @api.onchange('pdt_temp_ids')
    def _onchange_pdt_temp_ids(self):
        for rec in self:
            if rec.pdt_temp_ids:
                lines = [(5, 0, 0)]
                # lines = []
                # print("self.pdt_temp", self.pdt_temp.qc_params_line_ids)
                for line in self.pdt_temp_ids.qc_params_line_ids:
                    val = {
                        'questionss': line.questions,

                    }
                    lines.append((0, 0, val))
                rec.qc_line_idss = lines


    class QualityLiness(models.Model):
        _name = "quality.liness"

        snos = fields.Integer(string='Sno')
        questionss = fields.Char(string='Questions')
        ress =fields.Selection(
        [('p', 'Pass'), ('F', 'Fail')],
         string='Response',tracking=True)
        remarks = fields.Char(string="Remark",tracking=True)
        pas = fields.Boolean("Pass")


        qc_ids = fields.Many2one('custom.quality.check', string='Quality')


    class ProductQcLines(models.Model):
        _name = "product.quality.lines"


        product_id_line =fields.Many2one("product.product",string='Products')
        p_line_qs = fields.Char(string='Questions')

        # hide = fields.Boolean(string='Hide', compute="_compute_hide")

        p_line_lot_id = fields.Many2one("stock.production.lot",string='Lot Number')
        p_line_lot = fields.Char(string='Lot Number')
        p_qty = fields.Float(string='Quantity')
        p_responce =fields.Selection(
        [('p', 'Pass'), ('F', 'Fail')],
         string='Response',tracking=True)
        p_remarks = fields.Char(string="Remark",tracking=True)
        state = fields.Selection(
            [('d', 'Draft'), ('o', 'Ongoing'), ('c', 'Completed')],
            default='d', string='Status', tracking=True)
        pas = fields.Boolean("Pass")

        qc_p_ids = fields.Many2one('custom.quality.check', string='Product Quality')




    ##################    Sub contracting After

    class AfterQualityLiness(models.Model):
        _name = "after.qc.lines"

        no = fields.Integer(string='Sno')
        qstns = fields.Char(string='Questions')
        resp = fields.Selection(
            [('p', 'Pass'), ('F', 'Fail')],
            string='Response', tracking=True)
        remrk = fields.Char(string="Remark", tracking=True)
        pa = fields.Boolean("Pass")

        a_qc_ids = fields.Many2one('custom.quality.check', string='Subcontracting')

        # @api.depends('qc_p_ids.state')
        # def _compute_hide(self):
        #     for i in self.qc_p_ids:
        #         if i.state == "c":
        #             self.hide = True
        #         else:
        #             self.hide = False







    def action_ongoing(self):
        self.state = 'o'
        operations = self.env['stock.picking.type'].sudo().search(
                                                    [('name', 'like','Sub')])
        # print(operations.id)
        if self.op_type.id == operations.id:
            self.show_after = True

            for rec in self:
                if rec.pdt_temp_ids:
                    lines = [(5, 0, 0)]
                    # lines = []
                    # print("self.pdt_temp", self.pdt_temp.qc_params_line_ids)
                    for line in self.pdt_temp_ids.qc_after_params_ids:
                        val = {
                            'qstns': line.af_qs,

                        }
                        lines.append((0, 0, val))
                    rec.after_qc_line_ids = lines

        # self.qc_prdt_line_ids.state='o'

    def action_done(self):
        self.state = 'c'
        # self.qc_prdt_line_ids.state = 'c'


    ########################### Creating Transfer ######################
    #
    # def create_trnsfer(self):
    #     print("returned")
    # #








    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('custom.quality.check') or _('New')


        res = super(CustomQualityCheck, self).create(vals)
        return res

