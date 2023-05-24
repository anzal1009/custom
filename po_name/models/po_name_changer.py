from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger


class PMnameChange(models.Model):
    _inherit = "purchase.order"

    name = fields.Char('Order Reference', required=True, index=True, copy=False, default='New', readonly="0")






    def action_name_change(self):
        print("yess")
        # purchase = self.env['purchase.order'].search([('name', '=', self.name)], limit=1) or False
        # if purchase:
        #     name = fields.Char('Order Reference', required=True, index=True, copy=False, default='New', readonly="0")


    #
    # def create(self, vals):
    #     if vals.get('name', _('New')) == _('New'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order') or _('New')
    #     res = super(PMnameChange, self).create(vals)
    #     return res
