from odoo import api, models, fields, _


class ShopRecord(models.Model):
    _name = "medical.sales"

    name_seq = fields.Char(string='Invoice ID', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    # name = fields.Char(string='Customer Name')
    number = fields.Char(string='GST IN')
    product = fields.Text(string='Product')
    idate = fields.Date(string='Invoice Date')
    name = fields.Many2one('medical.staff', string='Sales Person')
    cname = fields.Char(string="Customer Name")
    sales_line_ids = fields.One2many('sales.line', 'sales_id', string='Sales line')
    # total=fields.Float(string='total',compute='total')
    note= fields.Text(string="note")
    # amount_tax=fields.Float(string="Tax")
    amount_total = fields.Float(string="Total")

    amount_untaxed=fields.Float(string="Sub total",compute="compute_amount_total")


class ShopRecordlines(models.Model):
    _name = "sales.line"

    sno = fields.Integer(string='Sno')
    product = fields.Many2one('medical.products', string='Product Name')
    qty = fields.Integer(string='Quantity')
    price = fields.Integer(string="Price")
    total = fields.Float(string="Sub Total",compute="compute_sub_total")

    sales_id = fields.Many2one('medical.sales', string='Sales')




    @api.depends('total','sales_line_ids')
    def compute_amount_total(self):
        for record in self:
            total_invoice = 0
            for line in record.sales_line_ids:
                total_invoice = record.total + line.total
                record.total_invoice = record.amount_untaxed
                return record.amount_untaxed





    @api.model
    def create(self, vals):
        # if not vals.get('note'):
        #         vals['note'] = 'New Patient'

        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('medical.sales') or _('New')
        res = super(ShopRecord, self).create(vals)
        return res

    @api.depends('qty','price')
    def compute_sub_total(self):
        for row in self:
            row.total = row.qty * row.price
            return row.total




    #
    # @api.depends('qty','price')
    # def compute_amount_total(self):
    #     for record in self:
    #         total_invoice = 0
    #         for line in record.sales_line_ids:
    #             total_invoice = total_invoice + (line.qty * line.price)
    #             record.amount_total = total_invoice

    # @api.depends('qty','price','sales_line_ids')
    # def compute_amount_total(self):
    #
    #     for r in self:
    #         amount_total = total = 0.00
    #         for line in r.sales_line_ids:
    #             r.amount_total = r.total + r.sales_line_ids(r.qty*r.price)
    #             return r.amount_total






    # @api.depends('sales_line.total')
    # def compute_amount_total(self):
    #     for num in self:
    #         amount_total=0
    #         for line in num.sales_line:
    #             amount_total=amount_total+num
    # #             return amount_total

    # @api.depends('sales_line_ids.total')
    #
    # def compute_total(self):
    #
    #     for val in self:
    #         total = 0
    #         for line in val.sales_line_ids:
    #             total += line.total
    #         val.update({
    #                 'total': total,
    #                 'amount_total':total,
    #         })





    # my_list = ['sales_line.total']





            # va.amount_total=va.qty * va.price
            # va.amount_total=va.total
            # return va.amount_total



        # amount_total=self.total
        # for val in self:
        #     val.amount_total=(val.qty * val.price)+ amount_total
        #     return val.amount_total




















    # @api.depends('sales_line')
    #
    # def compute_total_amount(self):
    #     for record in self:
    #         total= 0
    #         for line in record.sales_line:
    #             total_amount = line.qty * line.price
    #             record.compute_total_amount = total
