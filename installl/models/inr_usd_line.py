# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class AccountMoveLineCustomLineINRCur(models.Model):
    _inherit = "account.move.line"


    cost_in_inr_cur = fields.Monetary(string='Cost In INR', default=0.0, currency_field='company_currency_id',
                                      compute='_compute_cost_in_inr_cur')



    @api.depends('price_unit')
    def _compute_cost_in_inr_cur(self):
        for line in self:
            cost_in_inr_cur = line.credit
            line.cost_in_inr_cur = cost_in_inr_cur


class AccountMoveINRCur(models.Model):
    _inherit = "account.move"


    total_subtotal  = fields.Monetary(string='Untaxed Amount In INR', default=0.0, currency_field='company_currency_id',
                                      compute='_compute_subtotal_in_inr_cur')
    total_taxamount = fields.Monetary(string='Taxed Amount in INR', default=0.0, currency_field='company_currency_id',
                                     compute='_compute_tax_in_inr_cur')
    total_inr_amount = fields.Monetary(string='Total in INR', default=0.0, currency_field='company_currency_id',
                                      compute='_compute_total_in_inr_cur')

    @api.depends('amount_total')
    def _compute_subtotal_in_inr_cur(self):
        for line in self:
            total_subtotal = line.amount_untaxed_signed
            line.total_subtotal = total_subtotal

    @api.depends('amount_total')
    def _compute_tax_in_inr_cur(self):
        for line in self:
            total_taxamount = line.amount_tax_signed
            line.total_taxamount = total_taxamount

    @api.depends('amount_total')
    def _compute_total_in_inr_cur(self):
        for line in self:
            total_inr_amount = line.amount_total_signed
            line.total_inr_amount = total_inr_amount

