from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ManufactureOrder(models.Model):
    _inherit = 'mrp.production'


    def action_get_transfers(self):


        # MO Details

        # for item in self:
        #     for line in item.move_raw_ids:
        #         print(line.product_id.name)


        transfers =  self.env['stock.picking'].sudo().search([('ref', '=', "MO Transfer " + self.name)])
        for int in transfers:
            # print(int.name)
            if transfers:
                for lines in int.move_ids_without_package:
                    # print(lines.product_id.name)

                    for item in self:
                        for line in item.move_raw_ids:
                            # print(item.name)
                            # print(line.product_id.name)



                            if lines.product_id.id == line.product_id.id:
                                print("yesss")
                                print(line.product_id.name)

                                mo_lines = []

                                transfers = self.env['stock.picking'].sudo().search(
                                    [('ref', '=', "MO Transfer " + self.name)])
                                for int in transfers:
                                    for lines in int.move_ids_without_package:
                                        for tr_lot in lines.move_line_ids:
                                            m_line=(0,0,{
                                                'location_id': tr_lot.location_id.id,
                                                'location_dest_id': tr_lot.location_dest_id.id,
                                                'lot_id': tr_lot.lot_id.id,
                                                'qty_done': tr_lot.qty_done,
                                                'product_uom_id': tr_lot.product_uom_id.id
                                            }
                                                  )
                                            mo_lines.append(m_line)




                                for tr_lot in lines.move_line_ids:
                                    print("transfer lot")
                                    print(tr_lot.lot_id.name)

                                line.move_line_ids = mo_lines
















