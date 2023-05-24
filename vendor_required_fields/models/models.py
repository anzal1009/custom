# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    msme = fields.Char("Is a MSME")




    @api.constrains('credit_warning', 'credit_blocking', 'credit_check', 'supplier')
    def _check_credit_limit_checking_vendor(self):
        for credit in self:
            if credit.supplier:
                if not credit.credit_check:
                    raise ValidationError(_('Please activate credit limit.'))
                if credit.credit_warning <= 0 or credit.credit_blocking <= 0:
                    raise ValidationError(_('Warning amount or blocking amount should be greater than zero.'))

    @api.constrains('bank_ids', 'supplier')
    def _check_bank_details_vendor(self):
        for record in self:
            if record.supplier:
                if not record.bank_ids:
                    raise ValidationError(_('Please provide bank details of supplier.'))


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    ifsc_code = fields.Char('IFSC')

    @api.onchange('bank_id')
    def load_bank_ifsc(self):
        for record in self:
            if record.bank_id and record.bank_id.ifs_code:
                record.ifsc_code = record.bank_id.ifs_code



