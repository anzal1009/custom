from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class CComplaints(models.Model):
    _name = 'cst.complaints'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))

    name = fields.Char("Customer Name")
    cdate = fields.Date("Date")
    mobile = fields.Char("Contact No",required="1")
    mail = fields.Char("Email",required="1")
    location = fields.Char("Location")
    product = fields.Many2one('product.product',"Product Name")
    responsible = fields.Many2one('res.users',"User Incharge",required="1")
    responsible_ids = fields.Many2many('res.users','cst_complaints_rel','user_id_rec', string="Responsible Users")
    note = fields.Text("Complaint")
    qty = fields.Integer("Quantity")
    sol = fields.Text("Solution")
    addrs = fields.Text("Address")
    lot = fields.Char("Lot Number")
    price = fields.Float(related='product.list_price' ,string="Price")

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)





    state = fields.Selection(
        [('d', 'Draft'),('r', 'Registered'),('s','Mail Send'),('i', 'Initiated'),('do', 'Done')],
        default='d', string='Status', tracking=True)

    def action_validte(self):
        self.state ='r'

    def action_initiated(self):
        self.state ='i'

    def action_done(self):
        self.state ='do'


    def action_send_email(self):

        print("email send")
        print(self.mail)
        template_id = self.env.ref('Customer_complaints.cst_complaints_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 's'

    def action_email_done(self):
        print("maildone")
        template_id = self.env.ref('Customer_complaints.cst_complaints_complete_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):

        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('cst.complaints') or _('New')
        res = super(CComplaints, self).create(vals)
        return res
