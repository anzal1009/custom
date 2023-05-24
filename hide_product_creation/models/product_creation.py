from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductInherit(models.Model):
    _inherit = "sale.order"




######################### No Line items rise Error ################################


class FieldInherit(models.Model):
    _inherit = "sale.order"

    # payment_term_id = fields.Many2one(
    #     'account.payment.term', string='Payment Terms', check_company=True,  # Unrequired company
    #     domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", readonly=True, store=True,force_save=True )

    @api.constrains('order_line')
    def oder_line_val(self):
        for rec in self:
            if not self.order_line:
                raise ValidationError("Please Add Line Items.")




class LineInherit(models.Model):
    _inherit = "sale.order.line"

    name = fields.Text(string='Description', required=True, states={'sale': [('readonly', True)],'cancel': [('readonly', True)], 'done': [('readonly', True)]})




class LineLessSave(models.Model):
    _inherit = "purchase.order"

    @api.constrains('order_line')
    def oder_line_pur_val(self):
        for rec in self:
            if not self.order_line:
                raise ValidationError("Please Add Line Items.")



class LinePurchaseInherit(models.Model):
    _inherit = "purchase.order.line"

    name = fields.Text(string='Description', required=True , states={'purchase': [('readonly', True)],'cancel': [('readonly', True)], 'done': [('readonly', True)]})



