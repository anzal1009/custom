from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritLot(models.Model):
    _inherit = 'stock.production.lot'

    lot_cost = fields.Float(compute='_compute_unit_cost', string="Lot Cost")
    lot_cost_copy = fields.Float(string="Lot Cost")
    total_cost = fields.Float(string="Total Cost")
    lot_total = fields.Float(compute='_compute_total_val', string="Actual Stock Value")


    def _compute_unit_cost(self):
        for data in self:
            # data.action_view_po()
            stck_line = self.env['stock.move.line'].sudo().search(
                [('lot_name', '=', data.name,), ('company_id', '=', data.company_id.id)]) or False
            if stck_line:
                sum = 0
                val = 0
                for stk in stck_line:
                    cost = stk.move_id.price_unit
                    sum = sum + cost
                    val = val + 1
                    avg = sum / val
                self.lot_cost = avg
                self.lot_cost_copy = avg

            else:
                mo_details = self.env['mrp.production'].sudo().search(
                    [('lot_producing_id', '=', self.id,), ('company_id', '=', self.company_id.id)]) or False
                print("mo details", mo_details)
                if mo_details:
                    for i in mo_details:
                        stock_move = self.env['stock.move'].sudo().search(
                            [('production_id', '=', i.id,),('product_id','=',i.product_id.id),('company_id', '=', self.company_id.id)]) or False
                        # print(stock_move)
                        stock_val = self.env['stock.valuation.layer'].sudo().search(
                            [('stock_move_id', '=', stock_move.id,), ('company_id', '=', self.company_id.id)]) or False
                        # print("valu layer", stock_val.id)
                        if stock_val:
                            data.lot_cost = stock_val.unit_cost
                            data.lot_cost_copy = stock_val.unit_cost

                        else:
                            data.lot_cost = 0

                else:
                    data.lot_cost = 0

    @api.depends('product_qty')
    def _compute_total_val(self):
        for val in self:
            val.lot_total = val.product_qty * val.lot_cost


####################################   Valuation Layer   ###########################################


class StockValuationLayerInh(models.Model):
    _inherit = 'stock.valuation.layer'

    lot_id = fields.Char(compute='_compute_lot', string="Lot Number", store=True)
    cost_of_lot = fields.Float( string="Cost For Lot", store=True)
    lot_name_id = fields.Many2one("stock.production.lot", string="Lot Id", store=True)

    cost = fields.Float(string="Lot Cost",related ='lot_name_id.lot_cost_copy')
    tot_lot_val = fields.Monetary(compute='_compute_total_lot_value',string="Total Value",store=True)



    @api.depends('quantity')
    def _compute_lot(self):
        for lot in self:
            stock_mo = self.env['stock.move'].sudo().search(
                [('id', '=', lot.stock_move_id.id,), ('company_id', '=', self.company_id.id)]) or False
            #
            # if stock_mo:
            #     stk_mov_line = self.env['stock.move.line'].sudo().search(
            #         [('move_id', '=', stock_mo.id), ('product_id', '=', stock_mo.product_id.id),
            #          ('company_id', '=', self.company_id.id)]) or False
            #     print("lot name", stk_mov_line.lot_id.name)
            #     for ll in stk_mov_line:
            #         lot.lot_id = ll.lot_id.name
            #         lot.lot_name_id = ll.lot_id.id
            #
            #         if lot.lot_name_id:
            #             lot_n = self.env['stock.production.lot'].sudo().search([('id', '=',ll.lot_id.id)]) or False
            #
            #             if lot_n:
            #                 lot.cost_of_lot =lot_n.lot_cost
            #
            #
            #     # print("cost",stk_mov_line.lot_id.lot_cost)
            #     # lot.cost_of_lot = stk_mov_line.lot_id.lot_cost_copy
            # else:
            #     lot.lot_id = "nill"

    def action_done(self):
        for total in self:
            total.tot_lot_val = total.cost_of_lot * total.quantity

        # for lot in self:
        #     stock_mo = self.env['stock.move'].sudo().search(
        #         [('id', '=', lot.stock_move_id.id,), ('company_id', '=', self.company_id.id)]) or False
        #
        #     if stock_mo:
        #         stk_mov_line = self.env['stock.move.line'].sudo().search(
        #             [('move_id', '=', stock_mo.id), ('product_id', '=', stock_mo.product_id.id),
        #              ('company_id', '=', self.company_id.id)]) or False
        #         print("lot name", stk_mov_line.lot_id.name)
        #         for ll in stk_mov_line:
        #             lot.lot_id = ll.lot_id.name
        #             lot.lot_name_id = ll.lot_id.id
        #
        #             if lot.lot_name_id:
        #                 lot_n = self.env['stock.production.lot'].sudo().search([('id', '=', ll.lot_id.id)],limit=1) or False
        #
        #                 if lot_n:
        #                     lot.cost_of_lot = lot_n.lot_cost
        #
        #         # print("cost",stk_mov_line.lot_id.lot_cost)
        #         # lot.cost_of_lot = stk_mov_line.lot_id.lot_cost_copy
        #     else:
        #         lot.lot_id = "nill"

    # @api.depends('lot_name_id')
    # def _compute_cost_of_lot(self):
    #     for cost in self:
    #         if cost.cost_of_lot == 0.00:
    #             lot_name = self.env['stock.production.lot'].sudo().search(
    #                 [('id', '=', cost.lot_name_id.id), ('product_id', '=', cost.product_id.id),
    #                  ('company_id', '=', self.company_id.id)]) or False
    #             if lot_name:
    #                 # for k in lot_name:
    #                 cost.cost_of_lot = lot_name.lot_cost
    #             # else:
                #     cost.cost_of_lot = k.lot_cost




    @api.depends('quantity')
    def _compute_total_lot_value(self):
        for total in self:
            total.tot_lot_val = total.cost_of_lot * total.quantity










########################################


#             if stock_mo:
#                 stk_mov_line = self.env['stock.move.line'].sudo().search(
#                     [('move_id', '=', stock_mo.id), ('product_id', '=', stock_mo.product_id.id),
#                      ('company_id', '=', stock_mo.company_id.id)], limit=1) or False
# #                 for st in stk_mov_line:
#                 lot.lot_id = stk_mov_line.lot_id.name
#                 lot.lot_name_id = stk_mov_line.lot_id.id

# #                 if lot.lot_name_id:
# #                     lot_n = self.env['stock.production.lot'].sudo().search([('id', '=', stk_mov_line.lot_id.id)]) or False
# #                     if lot_n:

# #                         lot.cost_of_lot = lot_n.lot_cost
#             else:
#                 lot.lot_id = "nill"

#     @api.depends('quantity')
#     def _compute_cost_of_lot(self):
#         for cost in self:
#             if cost.cost_of_lot == 0.00:
#                 lot_name = self.env['stock.production.lot'].sudo().search(
#                     [('id', '=', cost.lot_name_id.id), ('product_id', '=', cost.product_id.id),
#                      ('company_id', '=', cost.company_id.id)], limit=1) or False
#                 if lot_name:
#     #                 for k in lot_name:
#                     cost.cost_of_lot = lot_name.lot_cost
#     #             else:
#     #                 cost.cost_of_lot = k.lot_cost