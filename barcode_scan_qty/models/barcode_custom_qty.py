# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class barcodeCustom(models.Model):
    _inherit = 'stock.picking'

    is_quantity_updated = fields.Boolean(string="Is Quantity Updated",tracking=True,readonly=True )

    
    def action_calculate_qty(self):
        self.is_quantity_updated = True
        print(self.move_ids_without_package)
        for line_items in self.move_line_ids_without_package:
            # for item in line_items.move_ids:
            line_items.qty_done = line_items.carton_nos * line_items.carton_weight


# class barcodeCustomLine(models.Model):
#     _inherit = 'stock.move'

#     carton_nos = fields.Float("CTN Number",tracking=True,store=True,force_save="1",readonly=True,compute='_compute_carton_nos',)
#     carton_weight = fields.Float("CTN Weight", tracking=True, store=True, force_save="1",compute='_compute_carton_per_weight',)

#     @api.onchange('quantity_done')
#     def _onchange_quantity_done(self):
#         print(self.quantity_done)


#     @api.onchange('product_id')
#     def _compute_carton_per_weight(self):
#         for line_items in self:
#             if line_items.product_id:
#                 product = self.env['product.product'].sudo().search([('id', '=', line_items.product_id.id)], limit=1)
#                 line_items.carton_weight = product.net_ctn


#     @api.depends('quantity_done')
#     def _compute_carton_nos(self):
#         line_status = 0
#         for picking in self.picking_id:
#             if picking.is_quantity_updated == True:
#                 line_status = 1
#         if line_status == 0:
#             for line_items in self:
#                 line_items.carton_nos = line_items.quantity_done
#                 print("CTN")

                
class barcodeCustomMoveLine(models.Model):
    _inherit = 'stock.move.line'

    carton_nos = fields.Float("CTN Number",tracking=True,store=True,force_save="1",readonly=True,compute='_compute_carton_nos',)
    carton_weight = fields.Float("CTN Weight", tracking=True, store=True, force_save="1",compute='_compute_carton_per_weight',)

    @api.onchange('qty_done')
    def _onchange_quantity_done(self):
        print(self.qty_done)

    @api.onchange('lot_id')
    def _compute_carton_per_weight_by_lot(self):
        for line_items_lot in self:
            lot = self.env['stock.production.lot'].sudo().search([('id', '=', line_items_lot.lot_id.id)], limit=1)
            print("llll")




    @api.onchange('product_id')
    def _compute_carton_per_weight(self):
        for line_items in self:
            if line_items.product_id:
                product = self.env['product.product'].sudo().search([('id', '=', line_items.product_id.id)], limit=1)
                if product:
                    if product.categ_id.name == "Raw Materials - Dust":
                        line_items.carton_weight = 10
                    else:
                        line_items.carton_weight = product.product_tmpl_id.net_ctn


                print(product.categ_id.name)
                print(line_items.lot_id.net_lot_weight)


            # if product.categ_id.name == "Raw Materials - Dust":
                #     line_items.carton_weight = line_items.lot_id.net_lot_weight
                # if product.categ_id.name == "Raw Materials - Import Dust":
                #     line_items.carton_weight = line_items.lot_id.net_lot_weight
                # if product.categ_id.name == "Raw Materials - Import Leaf":
                #     line_items.carton_weight = line_items.lot_id.net_lot_weight
                # if product.categ_id.name == "Raw Materials - Leaf":
                #     line_items.carton_weight = line_items.lot_id.net_lot_weight
                # if product.categ_id.name == "Raw Materials":
                #     line_items.carton_weight = line_items.lot_id.net_lot_weight
                # else:

#     @api.onchange('qty_done')
#     def _compute_carton_per_weight(self):
#         for line_items in self:
#             if line_items.carton_weight == 0:
#                 product = self.env['product.product'].sudo().search([('id', '=', line_items.product_id.id)], limit=1)
#                 line_items.carton_weight = product.product_tmpl_id.net_ctn


    @api.depends('qty_done')
    def _compute_carton_nos(self):
        line_status = 0
        for picking in self.picking_id:
            if picking.is_quantity_updated == True:
                line_status = 1
        if line_status == 0:
            for line_items in self:
#                 product = self.env['product.product'].sudo().search([('id', '=', line_items.product_id.id)], limit=1)

                if line_items.product_id.product_tmpl_id.categ_id.name == "Raw Materials - Dust":
                    line_items.carton_nos = line_items.qty_done
                    line_items.carton_weight = line_items.lot_id.net_lot_weight
                elif line_items.product_id.product_tmpl_id.categ_id.name == "Raw Materials - Import Dust":
                    line_items.carton_nos = line_items.qty_done
                    line_items.carton_weight = line_items.lot_id.net_lot_weight
                elif line_items.product_id.product_tmpl_id.categ_id.name == "Raw Materials - Import Leaf":
                    line_items.carton_nos = line_items.qty_done
                    line_items.carton_weight = line_items.lot_id.net_lot_weight
                elif line_items.product_id.product_tmpl_id.categ_id.name == "Raw Materials - Leaf":
                    line_items.carton_nos = line_items.qty_done
                    line_items.carton_weight = line_items.lot_id.net_lot_weight
                elif line_items.product_id.product_tmpl_id.categ_id.name == "Raw Materials":
                    line_items.carton_nos = line_items.qty_done
                    line_items.carton_weight = line_items.lot_id.net_lot_weight
                else:
                    line_items.carton_nos = line_items.qty_done
                    line_items.carton_weight = line_items.product_id.product_tmpl_id.net_ctn
                    print("CTN")
                    print(line_items.product_id.product_tmpl_id.categ_id.name)
                    print(line_items.lot_id.net_lot_weight)

