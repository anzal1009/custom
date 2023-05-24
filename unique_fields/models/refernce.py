from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError



class AccountUnique(models.Model):
    _inherit = 'account.move'


    def action_post(self):
        print("triggered")
        for rec in self:
            # acc = self.env['account.move'].sudo().search([('state','=','posted')])
            if rec.move_type == "out_invoice":
                duplicate = self.env['account.move'].sudo().search([('state','=','posted'),('partner_id','=',self.partner_id.id),('ref','=',self.ref)])or False
                print(duplicate)
                if duplicate:
                    # print("yesss")
                    raise ValidationError("Customer Reference already exist for Customer")
                else:
                    res = super(AccountUnique, self).action_post()



            elif rec.move_type == "in_invoice":
                duplicate_bill = self.env['account.move'].sudo().search([('state','=','posted'),('partner_id','=',self.partner_id.id),('ref','=',self.ref)])or False
                print(duplicate_bill)
                if duplicate_bill:
                    # print("yesss")
                    raise ValidationError("Bill Reference already exist for Vendor")
                else:
                    res = super(AccountUnique, self).action_post()
            else:
                res = super(AccountUnique, self).action_post()


    # @api.constrains('ref')
    # def duplicate_reference(self):
    #     for rec in self:
    #         duplicate = self.env['account.move'].sudo().search([('move_type','=','in_invoice'),('partner_id','=',self.partner_id.id),('ref','=',self.ref)])
    #         if duplicate:
    #             raise ValueError("Reference No already exist")

