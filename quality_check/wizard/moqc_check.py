from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger

class MoqcWizard(models.TransientModel):
    _name = "moqc.wizrd"

    name = fields.Char("Category Name")
    poid = fields.Char("MO No")
    qdate = fields.Date("Date")
    user = fields.Many2one('res.users', 'User', required=True, index=True,
                           default=lambda self: self.env.user)

    pdt_temp = fields.Many2one('params.moqc', "Category Templates")
    moqc_wiz_line_idss = fields.One2many('moqc.wizrd.line', 'moqc_wiz_ids', string='QC line')


    def create_moqc(self):
        print("yess")


    @api.onchange('pdt_temp')
    def _onchange_pdt_temp(self):
        for rec in self:
            if rec.pdt_temp:
                lines = [(5, 0, 0)]
                # lines = []
                print("self.pdt_temp", self.pdt_temp.moqc_params_line_ids)
                for line in self.pdt_temp.moqc_params_line_ids:
                    val = {
                        'questionss': line.questions,

                    }
                    lines.append((0, 0, val))
                rec.moqc_wiz_line_idss = lines



class MoqcWizLines(models.TransientModel):
    _name = "moqc.wizrd.line"

    questionss = fields.Char(string='Questions')
    ress = fields.Char(string='Response', tracking=True)
    remarks = fields.Char(string="Remark", tracking=True)

    moqc_wiz_ids = fields.Many2one('moqc.wizrd', string='Quality')





