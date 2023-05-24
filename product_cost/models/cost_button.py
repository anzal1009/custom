from odoo import models, fields, api,_
from odoo.exceptions import ValidationError, UserError
from odoo import exceptions


class ConsolidatedLots:
    def __init__(self, product_id,product_name,lot,lot_qty,lot_purchase_rate, value, qty):
        self.product_id = product_id
        self.product_name = product_name
        self.lots = [lot]
        self.lot_qty = [lot_qty]
        self.lot_purchase_rate=[lot_purchase_rate]
        self.value = value
        self.qty = qty

class ManufactureOrder(models.Model):
    _inherit = 'mrp.production'


    def action_cost2(self):

        items_consolidated = {}
        cost_not_found = []
        for line in self.move_raw_ids:
            if line.quantity_done > 0:
                item_found = False
                for line2 in line.move_line_ids:
                    item_found = True
                    if line2.qty_done > 0:
                        lot_found = False
                        purchase_moves = self.env['stock.move'].sudo().search(
                            [('product_id', '=', line.product_id.id),('purchase_line_id','!=',False),('company_id', '=', self.company_id.id)],order='id DESC') or False

                        #if Purchase
                        if purchase_moves:
                            for purchase_move in purchase_moves:
                                stock_line= self.env['stock.move.line'].sudo().search(
                                [('move_id', '=',purchase_move.id),('lot_id','=',line2.lot_id.id),('company_id', '=', self.company_id.id)]) or False

                                if(stock_line):
                                    if purchase_move.purchase_line_id.price_unit > 0:
                                        lot_found=True
                                        # sv_found = False
                                        # for cons_sv in items_consolidated:
                                        if line.product_id.id in items_consolidated.keys():
                                            # sv_found = True
                                            cons_sv = items_consolidated[line.product_id.id]
                                            cons_sv.qty += line2.qty_done
                                            cons_sv.value += line2.qty_done * purchase_move.purchase_line_id.price_unit
                                            cons_sv.lots.append(line2.lot_id.name)
                                            cons_sv.lot_qty.append(line2.qty_done)
                                            cons_sv.lot_purchase_rate.append(purchase_move.purchase_line_id.price_unit)
                                            line.mrp_product_unit_cost = cons_sv.value/cons_sv.qty
                                        else:
                                            items_consolidated[line.product_id.id] =  ConsolidatedLots(line.product_id.id,line.product_id.name,line2.lot_id.name,line2.qty_done,purchase_move.purchase_line_id.price_unit, line2.qty_done * purchase_move.purchase_line_id.price_unit, line2.qty_done)
                                            line.mrp_product_unit_cost = purchase_move.purchase_line_id.price_unit
                                        break


                        #if not purchase
                        if not lot_found:
                            prod_moves = self.env['stock.move'].sudo().search(
                                [('product_id', '=', line.product_id.id), ('production_id', '!=', False),
                                 ('company_id', '=', self.company_id.id)],order='id DESC') or False
                            # if production
                            if prod_moves:
                                for prod_move in prod_moves:
                                    move_prod_lines = self.env['stock.move.line'].sudo().search(
                                        [('move_id', '=', prod_move.id), ('lot_id', '=', line2.lot_id.id),
                                         ('company_id', '=', self.company_id.id)]) or False

                                    if move_prod_lines:
                                        value =self.env['stock.valuation.layer'].sudo().search(
                                        [('stock_move_id', '=', prod_move.id),
                                         ('company_id', '=', self.company_id.id)]) or False

                                        if value:
                                            if value.unit_cost > 0:
                                                lot_found=True
                                                # sv_found = False
                                                # for cons_sv in items_consolidated:
                                                if line.product_id.id in items_consolidated.keys():
                                                    # sv_found = True
                                                    cons_sv = items_consolidated[line.product_id.id]
                                                    cons_sv.qty += line2.qty_done
                                                    cons_sv.value += line2.qty_done * value.unit_cost
                                                    cons_sv.lots.append(line2.lot_id.name)
                                                    cons_sv.lot_qty.append(line2.qty_done)
                                                    cons_sv.lot_purchase_rate.append(value.unit_cost)
                                                    line.mrp_product_unit_cost = cons_sv.value / cons_sv.qty
                                                else:
                                                    items_consolidated[line.product_id.id] =  ConsolidatedLots(line.product_id.id, line.product_id.name, line2.lot_id.name,
                                                                         line2.qty_done, value.unit_cost,
                                                                         line2.qty_done * value.unit_cost,
                                                                         line2.qty_done)
                                                    line.mrp_product_unit_cost = value.unit_cost
                                                break

                        if not lot_found:
                            cost_not_found.append({
                                'product_name': line.product_id.name,
                                'lot': line2.lot_id.name})
                            # sv_found = False
                            # for cons_sv in items_consolidated:
                            if line.product_id.id in items_consolidated.keys():
                                # sv_found = True
                                cons_sv = items_consolidated[line.product_id.id]
                                cons_sv.qty += line2.qty_done
                                cons_sv.value += 0
                                cons_sv.lots.append(line2.lot_id.name)
                                cons_sv.lot_qty.append(line2.qty_done)
                                cons_sv.lot_purchase_rate.append(0)
                            else:
                                items_consolidated[line.product_id.id] =  ConsolidatedLots(line.product_id.id, line.product_id.name, line2.lot_id.name,
                                                     line2.qty_done, 0,
                                                     0,
                                                     line2.qty_done)

                if not item_found:
                    cost_not_found.append({
                        'product_name': line.product_id.name,
                        'lot': 'not found'})
                    # sv_found = False
                    # for cons_sv in items_consolidated:
                    if line.product_id.id in items_consolidated.keys():
                        # sv_found = True
                        cons_sv = items_consolidated[line.product_id.id]
                        cons_sv.qty += line.quantity_done
                        cons_sv.value += 0
                        cons_sv.lots.append('not found')
                        cons_sv.lot_qty.append(0)
                        cons_sv.lot_purchase_rate.append(0)
                    else:
                        items_consolidated[line.product_id.id] =  ConsolidatedLots(line.product_id.id, line.product_id.name, 'not found',
                                             0, 0,
                                             0,
                                             line.quantity_done)

        # if cost_not_found:
        #     items =""
        #     for not_found in cost_not_found:
        #         items +=  "Cannot Fetch Unit Price for Product Name: " + not_found['product_name'] + "   Lot: " + not_found['lot'] +"\n\n"
        #
        #     items += "Item Details\n\n"
        #     for item in items_consolidated:
        #         print(item.product_name)
        #         items += "Product Name: " + str(item.product_name)+ "   Qty: " + str(item.qty) + "\n"
        #         items += "\tLot Name:\t\t\tQty:\t\t\tUnit Price\n"
        #         vals2=[]
        #         for i in range(0,len(item.lots)):
        #             items += "\t" + str(item.lots[i]) + "\t\t\t" + str(item.lot_qty[i])+ "\t\t\t" + str(item.lot_purchase_rate[i]) + "\n"

            # raise exceptions.UserError(items)
            #     for item in items_consolidated:

        if cost_not_found:
            lines = []
            for item in items_consolidated.items():
                for i in range(0, len(item[1].lots)):
                    vals = (0, 0, {
                        'product':item[1].product_name,
                        'qty': item[1].qty,
                        'lot': item[1].lots[i],
                        'lot_qty': item[1].lot_qty[i],
                        'price': item[1].lot_purchase_rate[i]
                    })
                    lines.append(vals)
            return {'type': 'ir.actions.act_window',
                    'name': _('Cannot Fetch'),
                    'res_model': 'mo.cost.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                    'context': {'default_mo_wiz_line_ids': lines}
                    }









