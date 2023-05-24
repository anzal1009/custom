from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.http import request


class AccountRevAmount(models.Model):
    _inherit = "account.move"

    ############################## Based on Total Amount #################################

    # def action_post(self):
    #     for cre in self:
    #         if cre.reversed_entry_id:
    #             invoice_name = cre.ref
    #             invoice_split_name = invoice_name.split(': ')
    #
    #             inv_name = invoice_split_name[1]
    #
    #             # for i in inv_name:
    #             invoice =  request.env['account.move'].sudo().search([('name', '=', inv_name)])
    #             total = invoice.amount_total
    #
    #             if total < self.amount_total:
    #                 raise ValidationError(("The Total Amount is greater than Invoice Value"))
    #             else:
    #                 res = super(AccountRevAmount, self).action_post()
    #                 return res
    #
    #
    #
    #         else:
    #             res = super(AccountRevAmount, self).action_post()
    #             return res

    ############################## Based on Unit Price #################################
    def action_post(self):
        for cre in self:
            if cre.reversed_entry_id:
                for line in cre.invoice_line_ids:

                    invoice_name = line.ref
                    invoice_split_name = invoice_name.split(': ')

                    inv_name = invoice_split_name[1]

                    invoice = request.env['account.move.line'].sudo().search([('move_name', '=', inv_name)])

                    for i in invoice:
                        if i.name:
                            if i.product_id == line.product_id:
                                if i.price_unit < line.price_unit:
                                    raise ValidationError("The Product Cost is HIgh")
                                else:
                                    res = super(AccountRevAmount, self).action_post()
                                    return res

            else:
                res = super(AccountRevAmount, self).action_post()
                return res


