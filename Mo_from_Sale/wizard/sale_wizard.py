from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger

class SaleWizard(models.TransientModel):
    _name = "sale.wizard"

    name = fields.Char("Name")
    user = fields.Many2one('res.users', 'User', required=True, index=True,
                           default=lambda self: self.env.user)
    sale_wiz_line_idss = fields.One2many('sale.wizard.line', 'sale_wiz_ids', string='MO line')


    def create_mo(self):
        print("yess")
        modetails = []
        for i in self.sale_wiz_line_idss:
            print(i.product)
            print(i.qty)

            product = i.product.id
            print(product)
            qty = i.qty

            if product:
                product_bom = request.env['mrp.bom'].sudo().search([('product_tmpl_id', '=',i.product.id )]) or False

                if product_bom:
                    print("bom found")

                    product_id = request.env['product.product'].sudo().search(
                        [('name', '=', i.product.name)], limit=1) or False
                    print(product_id)

                    vals ={
                        'product_id': product_id.id,
                        'bom_id': product_bom.id,
                        'product_qty': qty,
                        # 'qty_producing': qty,
                        'product_uom_id': product_id.uom_id.id,
                        # 'date_planned_start': date,
                        # 'move_raw_ids': move_raw_ids
                    }
                    modetails = self.env['mrp.production'].create(vals)
                    modetails._onchange_move_raw()
                    for rec in modetails.move_raw_ids:
                        modetails.action_confirm()
                        modetails.button_mark_done()

                        # for line in modetails.move_raw_ids:
                        #     for lines in line.move_line_ids:
                        #         lines.qty_done = line.product_uom_qty
                        #         print( lines.qty_done)
                        #         modetails.qty_producing = qty



                # if not product_bom:
                #     raise UserError("BOM not Found.")





class SaleWizLines(models.TransientModel):
    _name = "sale.wizard.line"

    product = fields.Many2one("product.template", string='Product')
    qty = fields.Char(string='Qty', tracking=True)
    remarks = fields.Char(string="Remark", tracking=True)

    sale_wiz_ids = fields.Many2one('sale.wizard', string='Quality')
