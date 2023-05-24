from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InventoryTransfer(models.Model):
    _inherit = 'stock.picking'
    ref = fields.Char(string="Reference")

class ManufactureOrder(models.Model):
    _inherit = 'mrp.production'
    def action_transfer(self):
        rm1 = 0
        pm1 = 0
        sfg1 = 0
        for line in self.move_raw_ids:
            pdtctg = line.product_id.categ_id.name
            if pdtctg == "Raw Materials - Dust":
                rm1 = 1
            if pdtctg == "Raw Materials - Import Dust":
                rm1 = 1
            if pdtctg == "Raw Materials - Import Leaf":
                rm1 = 1
            if pdtctg == "Raw Materials - Leaf":
                rm1 = 1
            if pdtctg == "SFG":
                sfg1 = 1
            if pdtctg == "Packing Materials":
                pm1 = 1
            if pdtctg == "Market Return":
                sfg1 = 1
        picking_type = self.env['stock.picking.type'].sudo().search(
            [('name', '=', 'Internal Transfers'), ('company_id.id', '=', self.company_id.id)], limit=1) or False
        value = self.env['stock.picking'].sudo().search(
            [('ref', '=', "MO Transfer " + self.name), ('ref', '=', "MO Transfer " + self.name)])
        if value:
            raise ValidationError("Transfer Already Initiated. Please Check Inventory Transfers")
        dest_loc = self.env['stock.location'].sudo().search([('name', 'like', 'Process'), ('company_id.id', '=', self.company_id.id)], limit=1)
        loc_sfg = self.env['stock.location'].sudo().search([('name', 'like', 'Semi Finished'), ('company_id.id', '=', self.company_id.id)], limit=1)
        loc_pm = self.env['stock.location'].sudo().search([('name', 'like', 'Packing Material'), ('company_id.id', '=', self.company_id.id)], limit=1)
        loc_rm = self.env['stock.location'].sudo().search([('name', 'like', 'Raw Material'), ('company_id.id', '=', self.company_id.id)], limit=1)

        if sfg1==1:
            picking_sfg = self.env['stock.picking'].sudo().create({
                'location_id': loc_sfg.id,
                'location_dest_id': dest_loc.id,
                # 'partner_id': self.test_partner.id,
                'picking_type_id': picking_type.id,
                'immediate_transfer': False,
                'ref': "MO Transfer " + self.name,
                'origin': "MO Transfer " + self.name,
                'scheduled_date':  self.date_planned_start,
            })

        if pm1==1:
            picking_pm = self.env['stock.picking'].sudo().create({
                'location_id': loc_pm.id,
                'location_dest_id': dest_loc.id,
                # 'partner_id': self.test_partner.id,
                'picking_type_id': picking_type.id,
                'immediate_transfer': False,
                'ref': "MO Transfer " + self.name,
                'origin': "MO Transfer " + self.name,
            })

        if rm1==1:
            picking_rm = self.env['stock.picking'].sudo().create({
                'location_id': loc_rm.id,
                'location_dest_id': dest_loc.id,
                # 'partner_id': self.test_partner.id,
                'picking_type_id': picking_type.id,
                'immediate_transfer': False,
                'ref': "MO Transfer " + self.name,
                'origin': "MO Transfer " + self.name,
            })

        move_raw_ids = []
        for line in self.move_raw_ids:

            pdtctg = line.product_id.categ_id.name
            pdt_id = line.product_id.name
            if pdtctg == 'Market Return':

                move_receipt_sfg = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_sfg.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_sfg.id,
                    'location_dest_id': dest_loc.id,
                })
            
            if pdtctg == 'SFG':

                move_receipt_sfg = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_sfg.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_sfg.id,
                    'location_dest_id': dest_loc.id,
                })

                # sfg_line_cnt=sfg_line_cnt+1

            if pdtctg == 'Packing Materials':

                move_receipt_pm = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_pm.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_pm.id,
                    'location_dest_id': dest_loc.id,
                })

                # pm_line_cnt=pm_line_cnt+1

            if pdtctg == 'Raw Materials - Import Dust':

                move_receipt_rmi = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_rm.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_rm.id,
                    'location_dest_id': dest_loc.id,
                })

            if pdtctg == 'Raw Materials - Dust':
                move_receipt_rmd = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_rm.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_rm.id,
                    'location_dest_id': dest_loc.id,
                })

            if pdtctg == 'Raw Materials - Import Leaf':
                move_receipt_rmil = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_rm.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_rm.id,
                    'location_dest_id': dest_loc.id,
                })

            if pdtctg == 'Raw Materials - Leaf':
                move_receipt_rml = self.env['stock.move'].sudo().create({
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    # 'quantity_done': line["qty_done"],
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking_rm.id,
                    'picking_type_id': picking_type.id,
                    'location_id': loc_rm.id,
                    'location_dest_id': dest_loc.id,
                })
