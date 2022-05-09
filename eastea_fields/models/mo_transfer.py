from odoo import models, fields, api



class InventoryTransfer(models.Model):
    _inherit = 'stock.picking'

    ref = fields.Char(string="Reference")


class ManufactureOrder(models.Model):
    _inherit = 'mrp.production'






    def action_transfer(self):


        dest_loc_sfg = self.env['stock.location'].search([('name', '=', 'SFG')])
        print(dest_loc_sfg.id)


        picking_sfg = self.env['stock.picking'].create({
            'location_id': dest_loc_sfg.id,
            'location_dest_id': 35,
            # 'partner_id': self.test_partner.id,
            'picking_type_id': 5,
            'immediate_transfer': False,
            'ref': "MO Transfer " + self.name,
        })

        dest_loc_pm = self.env['stock.location'].search([('name', '=', 'Packing Materials')])
        print(dest_loc_pm.id)

        picking_pm = self.env['stock.picking'].create({
            'location_id': dest_loc_pm.id,
            'location_dest_id': 35,
            # 'partner_id': self.test_partner.id,
            'picking_type_id': 5,
            'immediate_transfer': False,
            'ref': "MO Transfer " + self.name,
        })

        move_raw_ids = []

        sfg_line_cnt = 0
        pm_line_cnt = 0
        move_receipt_sfg=0
        move_receipt_pm=0

        for line in self.move_raw_ids:

            pdtctg = line.product_id.categ_id.name
            pdt_id = line.product_id.name
            print(pdt_id)

            if pdtctg == 'SFG':

                move_receipt_sfg=self.env['stock.move'].create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': self.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': 1,
                    'picking_id': picking_sfg.id,
                    'picking_type_id': 5,
                    'location_id': dest_loc_sfg.id,
                    'location_dest_id': 35,
                })

                # sfg_line_cnt=sfg_line_cnt+1

            if pdtctg == 'Packing Materials':

                move_receipt_pm=self.env['stock.move'].create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': self.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': 1,
                    'picking_id': picking_pm.id,
                    'picking_type_id': 5,
                    'location_id': dest_loc_pm.id,
                    'location_dest_id': 35,
                })

                # pm_line_cnt=pm_line_cnt+1

























