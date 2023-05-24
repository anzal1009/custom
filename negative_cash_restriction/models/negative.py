from odoo import models, fields, api
from odoo.exceptions import ValidationError




class FieldModification(models.Model):
    _inherit = "account.move.line"
    #
    # @api.onchange('debit')
    # def on_change_debit(self):
    #     if self.debit:
    #         if self.move_id.move_type == "entry":
    #             balance = self.account_id.current_balance
    #             print(balance)
    #             print(self.account_id.name)
    #             print(self.debit)
    #             # if balance - self.debit == 0:
    #             #     raise ValidationError("Please Add Positive Amount.")
    #             amount = balance - self.debit
    #             print(amount)
    #             # if amount == '0':
    #             #     raise ValidationError("The current Account has insufficient Balance.")





    # @api.onchange('credit')
    @api.constrains('credit')
    def on_change_credit(self):
        for rec in self:
            if rec.credit:

                if rec.move_id.move_type == "entry":
                    print(rec.account_id.user_type_id.name)
                    if rec.account_id.name == "Cash":

                        balance = rec.account_id.current_balance
                        # if balance - self.credit == 0:
                        #     raise ValidationError("Please Add Positive Amount.")
                        amount = balance - rec.credit
                        # print(amount)
                        if  amount < 0:
                            raise ValidationError("The current Account has insufficient Balance.")






