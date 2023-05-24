from odoo import models,fields,api



class StatusInherited(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

