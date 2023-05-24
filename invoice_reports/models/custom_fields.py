import logging

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError,ValidationError
# from num2words import num2words
import  locale
try:
    from num2words import num2words
except ImportError:
    num2words = None




class ReportFields(models.Model):

    _inherit = "account.move"

    # vessal = fields.Char("Vessel/Flight No.")
    loading = fields.Char("Port of Loading")
    discharge = fields.Char("Port of Discharge")
    destination = fields.Char("Final Destination")
    mode = fields.Char("Transport Mode")
    package = fields.Char("No. & Kind of Pkgs")
    terms = fields.Char("Terms of Delivery and Payment")
    cariage = fields.Char("Pre-carriage by")
    container = fields.Char("CONTAINER No ")
    eseal = fields.Char(" E SEAL")
    gross = fields.Char("Gross Weight")
    net = fields.Char("Net Weight")
    cubic = fields.Char("Cubic Metres")

    text_amount_ar = fields.Char(string="Montant", required=False, compute="amount_to_words")


    def action_check_adrs(self):
        print("yess")



    def amount_to_text(self, amount,currency_id):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang='en_IN').title()
            except NotImplementedError:
                return num2words(number, lang='en_IN').title()



    @api.depends('amount_untaxed')
    def amount_to_words(self):
        for record in self:
            currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
            if currency_id:
                record.text_amount_ar = self.amount_to_text(record.amount_untaxed, currency_id)

                print(record.text_amount_ar)

    # def amount_to_words(self):
    #     for rec in self:
    #         if rec.amount_untaxed:
    #             rec.text_amount_ar = num2words(rec.amount_untaxed, to='currency', lang='en_IN')
    def amount_to_text(self, amount, currency_id, _name_=None):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang='en_IN').title()
            except NotImplementedError:
                return num2words(number, lang='en_IN').title()

        if num2words is None:
            logging.getLogger(_name_).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(currency_id.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].search([('code', '=', lang_code)])
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
            amt_value=_num2words(integer_value, lang=lang.iso_code),
            amt_word=currency_id.currency_unit_label,
        )
        if not currency_id.is_zero(amount - integer_value):
            amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(
                amt_value=_num2words(fractional_value, lang=lang.iso_code),
                amt_word=currency_id.currency_subunit_label,
            )
        if amount_words:
            amount_words = amount_words
        return amount_words


                # print(rec.text_amount_ar)

        # for record in self:
        #     currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        #     if currency_id:
        #         record.text_amount_ar = self.amount_to_text(record.amount_untaxed, currency_id)
        #         print(record.text_amount_ar)

    # total_usd_words = fields.Char(string="Total Net Amount in USD", compute='_compute_amount_totalusd_words',
    #                               store=True)

    # @api.multi
    # def amount_to_text(self,amount_untaxed , currency='Euro'):
    #     return amount_to_text(amount_untaxed, currency)

    #
    # @api.depends('invoice_line_ids')
    # def _compute_amount_totalusd_words(self):
    #     """
    #     To find amount total in words.
    #     """
    #     for record in self:
    #         currency_id = self.env['res.currency'].search([('name','=','USD')],limit=1)
    #         if currency_id:
    #             record.total_usd_words = self.amount_to_text(self.amount_untaxed,currency_id)
    #             print( record.total_usd_words)
    #
    #


