from odoo import api, models, _

class InventoryAgingReport(models.AbstractModel):
    _name = 'report.inventory_aging.inv_age_report_temp'
    _description = 'Inventory Aging Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("i am In")
        print("doc", docids)
        print("self", self)

        docs = self.env['stock.quant'].browse(docids[0])
        # products = self.env['product.product'].search([])

        stock = self.env['stock.quant'].search([])
        # print(products)
        # products_list = []
        stock_list = []


        for stk in stock:

            # stck_line = self.env['stock.move.line'].sudo().search(
            #     [('product_id', '=', stk.product_id.id),('lot_name', '=', stk.lot_id.name), ('company_id', '=', stk.company_id.id)]) or False
            # if stck_line:
            #     sum = 0
            #     val = 0
            #     for stk_lines in stck_line:
            #         # print(stk_line.move_id.price_unit)
            #         cost = stk_lines.move_id.price_unit
            #         sum = sum + cost
            #         val = val + 1
            #         avg = sum / val
            #         print(avg)


            data = {
                'product_id': stk.product_id.name,
                'quantity': stk.quantity,
                'location_id': stk.location_id.name,
                'lot_id': stk.lot_id.name,
                # 'price': avg,
                # 'appointment_date': app.appointment_date
            }
            stock_list.append(data)



        # for app in products:
        #     vals = {
        #         'name': app.name,
        #         # 'notes': app.notes,
        #         # 'appointment_date': app.appointment_date
        #     }
        #     products_list.append(vals)
        #
        #     print(products_list)


        return {
            'doc_model': 'stock.quant',
            'docs': docs,
            # 'products_list': products_list,
            'stock_list': stock_list,
        }


