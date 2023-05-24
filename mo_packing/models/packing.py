from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class MoPacking(models.Model):
    _name = 'mrp.packing'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name_seq = fields.Char(string='Number', required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    name = fields.Char('Product Name')
    qty = fields.Integer('Total Quantity')
    lot = fields.Char('Lot Number')
    pqty = fields.Float('Quantity Per Package(kg)', tracking=True)
    nqty = fields.Float('Net Quantity',readonly=True,store=True ,force_save="1")
    carton =fields.Integer('Units in Carton', tracking=True)
    cono =fields.Integer('No of Cartons',readonly=True,store=True,force_save="1")
    loc = fields.Many2one('stock.location',"Source Location", tracking=True)
    values = fields.Char("Packing Type")


    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    state = fields.Selection(
        [('d', 'Draft'),('v', 'Validated'), ('do', 'Done')],
        default='d', string='Status', tracking=True)

    sales_line_ids = fields.One2many('mrp.packing.line', 'sales_id', string='Sales line')

    @api.onchange('pqty')
    def onchange_compute_pqty(self):
        if self.pqty:
            self.nqty = self.qty / self.pqty

    @api.onchange('carton')
    def onchange_compute_carton(self):
        if self.carton:
            self.cono = self.nqty / self.carton

    class Salesline(models.Model):
        _name = "mrp.packing.line"

        sno = fields.Char(string='Sno')
        carton_name = fields.Char('Carton Name')
        barcode = fields.Char (string='Barcode')
        sales_id = fields.Many2one('mrp.packing', string='Sales')

    def action_validte(self, **rec):
        print("hiii")
        print(self.cono)
        if self.values:
            packages = self.values * self.cono
            print(packages)
            for l in self.sales_line_ids:
                l.carton_name = packages
                print(l.carton_name)



            # order_line = []
            #
            # order_line.append((0, 0, {
            #     'carton_name': packages,
            # }))
            # print('yyyyy')
            #
            # sale_order_1 = request.env['mrp.packing'].sudo().create({
            #
            #     'sales_line_ids': order_line,
            #
            # })
            # print('ooo')
            # request.env.cr.commit()



        # value = "Carton"
        # print(value)
        # def string_print(cono):
        #     for y in range(self.cono):
        #         print(value)

        # string_print(self.cono)
        #     sales_line_ids.append((0,0,{
        #         'carton_name': string_print(self.cono)
        #
        #     }))


            # carton_details = {
            #     'carton_name': string_print(self.cono)
            #
            # }
            # add_product = request.env['mrp.packing.line'].sudo().create(carton_details)



        # def print_string(cono):

        #         print("yes")
        # for x in range(self.cono):
        #     print(x)
        # nme = "Carton"
        # number = int("01")
        # for i in range(1, number + 1):
        #     print(i, end='  ')
        #     cart = nme + number
        #     print(cart)
        # for i in rec (self.cono):
        #     self.sale_line_ids.append((0, 0, {
        #                   'carton_name':"00002"
        #                 }))












    def action_barcode(self):
        print("hello")

    @api.model

    def create(self, vals):
        # if not vals.get('note'):
        #         vals['note'] = 'New Patient'

        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('mrp.packing') or _('New')
        res = super(MoPacking, self).create(vals)
        return res
