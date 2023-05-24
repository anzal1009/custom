



from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger



class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move'

    price = fields.Float("Price",tracking=True,store=True,force_save="1",readonly=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:

            # for lines in self:
            for mas in self.picking_id:
                # if mas.price_list:
                pr_list= self.env['product.pricelist'].sudo().search([('id','=',mas.price_list.id)])
                # print(pr_list.name)

                # if pr_list:
                for li in pr_list:
                    for pi in li.item_ids:
                        # print(self.product_id.name)
                        # print(pi.product_tmpl_id.name)
                        if self.product_id.name == pi.product_tmpl_id.name:
                            self.price = pi.fixed_price

                        else:
                            if self.price == 0.00:
                                self.price = self.product_id.standard_price


                        # else:
                        #     product = self.env['product.product'].sudo().search([('id', '=', self.product_id.id)])
                        #     self.price = product.list_price

                        # elif self.product_id.name != pi.product_tmpl_id.name:
                        #     self.price = self.product_id.list_price

                        # print(self.price)
                            # print(pi.fixed_price)



class PriceList(models.Model):
    _inherit = "stock.picking"

    price_list= fields.Many2one("product.pricelist","Price list" ,tracking=True, store=True,force_save="1")

    @api.onchange('price_list')
    def onchange_price_list(self):
        if self.price_list:

            price = self.env['product.pricelist'].sudo().search([('id', '=', self.price_list.id)])
            # print(price.name)
            # if price:
            for p in price:
                for pr in p.item_ids:
                    # print(pr.fixed_price)
                    for i in self:
                        for k in i.move_ids_without_package:
                            if k.product_id.name == pr.product_tmpl_id.name:
                                # print(k.product_id.name == pr.product_tmpl_id.name)
                                k.price = pr.fixed_price
                            else:
                                if k.price == 0.00:
                                    k.price = k.product_id.standard_price




                            #     product = self.env['product.product'].sudo().search([('id', '=', k.product_id.id)])
                            #     k.price = product.list_price


                                    # request.env.cr.commit()
                        #         if not k.product_id.name == pr.product_tmpl_id.name:
                        #             k.price = self.product_id.list_price
                        #         elif k.product_id.name != pr.product_tmpl_id.name:
                        #             k.price = self.product_id.list_price








