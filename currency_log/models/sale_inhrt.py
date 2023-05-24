from odoo import models, fields, api,_






class SaleCurrency(models.Model):
    _inherit = 'sale.order'

    usd_rate =fields.Float(string='Currency Rate',store=True)

    @api.onchange('pricelist_id', 'date_order')
    def _compute_usd_rate(self):

        if self.pricelist_id:
            print(self.currency_id.symbol)
            if self.currency_id.name == "INR":
                self.usd_rate = "01"
            else:
                sale_date = self.date_order
                date = sale_date.date()

                date_in_rate = self.env['res.currency.rate'].sudo().search(
                    [('name', '=', date), ('company_id', '=', self.company_id.id)], limit=1) or False

                if date_in_rate:
                    self.usd_rate = date_in_rate.inverse_company_rate
                    print(date_in_rate.inverse_company_rate)

                else:
                    self.usd_rate = False





class InvoiceCurrency(models.Model):
    _inherit = 'account.move'

    usd_rates =fields.Float(string='Currency Rate',readonly=True)

    @api.onchange('currency_id', 'invoice_date')
    def onchange_currency_rate(self):
        if self.move_type =="out_invoice":
            if self.currency_id.name == "INR":
                self.usd_rates = "01"
            else:
                date = self.invoice_date

                date_in_rate = self.env['res.currency.rate'].sudo().search(
                    [('name', '=', date), ('company_id', '=', self.company_id.id)], limit=1) or False

                if date_in_rate:
                    print("Date found", date_in_rate)

                    self.usd_rates = date_in_rate.inverse_company_rate
                    print(self.usd_rates)
                else:
                    self.usd_rates = False
                    print("Date not found ")




    # @api.depends('currency_id','invoice_date')
    # def _compute_usd_rates(self):
    #     if self.move_type =="out_invoice":
    #         if self.currency_id.name == "INR":
    #             self.usd_rates = "01"
    #         else:
    #             date = self.invoice_date
    #
    #             date_in_rate = self.env['res.currency.rate'].sudo().search(
    #                 [('name', '=', date), ('company_id', '=', self.company_id.id)], limit=1) or False
    #
    #             if date_in_rate:
    #                 print("Date found", date_in_rate)
    #
    #                 self.usd_rates = date_in_rate.inverse_company_rate
    #                 print(self.usd_rates)
    #             else:
    #                 self.usd_rates = False
    #                 print("Date not found ")




class PaymentCurrency(models.Model):
    _inherit = 'account.payment'

    usds_rates =fields.Float(string='Currency Rate',store=True)

    @api.onchange('currency_id', 'date')
    def _compute_usds_rates(self):
        if self.currency_id.name == "INR":
            self.usd_rates = "01"
        else:
            date = self.date

            date_in_rate = self.env['res.currency.rate'].sudo().search(
                [('name', '=', date), ('company_id', '=', self.company_id.id)], limit=1) or False

            if date_in_rate:
                print("Date found", date_in_rate)

                self.usds_rates = date_in_rate.inverse_company_rate
                print(self.usds_rates)
            else:
                self.usds_rates = False
                print("Date not found ")









