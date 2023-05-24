
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliver_to = fields.Many2one('res.partner', string='Deliver To',
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    def _prepare_invoice(self):
        res = super(SaleOrder,self)._prepare_invoice()
        res.update({
            'deliver_to': self.deliver_to,
        })
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    vehicle_no = fields.Char("Vehicle No.")
    deliver_to = fields.Many2one('res.partner', string='Deliver To',
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    details_in_invoice_print = fields.Boolean('In Invoice Print', default=False)


class ResBank(models.Model):
    _inherit = "res.bank"

    ifs_code = fields.Char('IFSC')


class ResCompany(models.Model):
    _inherit = "res.company"

    company_in_print = fields.Char('Company Name in Print')



