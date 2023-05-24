from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning



class SaleQtyTotal(models.Model):
    _inherit = 'sale.order'

    total_qty_kg = fields.Float(string="Total Ordered Kg" ,compute='_compute_kg_quantity', digits=0)
    total_qty_nos = fields.Float(string="Total Ordered Nos" ,compute='_compute_nos_quantity', digits=0)
    total_qty_lit = fields.Float(string="Total Ordered Liter" ,compute='_compute_lit_quantity', digits=0)
    total_qty_units = fields.Float(string="Total Ordered Units" ,compute='_compute_unit_quantity', digits=0)
    # total_qty_lit = fields.Float(string="Total Ordered Liter" ,compute='_compute_lit_quantity', digits=0)
    # t_qty = fields.Char("qty" ,compute='_compute_sum_quantity')


    @api.depends('order_line.product_uom_qty')
    def _compute_kg_quantity(self):
        for order in self:
            qty_kg = 0
            for line in order.order_line:
                # unit = line.product_uom.name
                if line.product_uom.name == "kg":
                    qty_kg += line.product_uom_qty
                elif line.product_uom.name == "Kg":
                    qty_kg += line.product_uom_qty
            order.total_qty_kg = qty_kg

    @api.depends('order_line.product_uom_qty')
    def _compute_nos_quantity(self):
        for order in self:
            qty_nos = 0
            for line in order.order_line:
                if line.product_uom.name == "Nos":
                    qty_nos += line.product_uom_qty
            order.total_qty_nos = qty_nos

    @api.depends('order_line.product_uom_qty')
    def _compute_lit_quantity(self):
        for order in self:
            qty_ltr = 0
            for line in order.order_line:
                if line.product_uom.name == "L":
                    qty_ltr += line.product_uom_qty
            order.total_qty_lit = qty_ltr

    @api.depends('order_line.product_uom_qty')
    def _compute_unit_quantity(self):
        for order in self:
            qty_unit = 0
            for line in order.order_line:
                if line.product_uom.name == "Units":
                    qty_unit += line.product_uom_qty
            order.total_qty_units = qty_unit





class PurchaseQtyTotal(models.Model):
    _inherit = 'purchase.order'

    total_pur_qty_kg = fields.Float(string="Total Ordered Kg", compute='_compute_pur_kg_quantity', digits=0)
    total_pur_qty_nos = fields.Float(string="Total Ordered Nos", compute='_compute_pur_nos_quantity', digits=0)
    total_pur_qty_lit = fields.Float(string="Total Ordered Liter", compute='_compute_pur_lit_quantity', digits=0)
    total_pur_qty_units = fields.Float(string="Total Ordered Units", compute='_compute_pur_unit_quantity', digits=0)



    @api.depends('order_line.product_uom_qty')
    def _compute_pur_kg_quantity(self):
        for order in self:
            qty_kg = 0
            for line in order.order_line:
                # unit = line.product_uom.name
                if line.product_uom.name == "kg":
                    qty_kg += line.product_uom_qty
                elif line.product_uom.name == "Kg":
                    qty_kg += line.product_uom_qty
            order.total_pur_qty_kg = qty_kg

    @api.depends('order_line.product_uom_qty')
    def _compute_pur_nos_quantity(self):
        for order in self:
            qty_nos = 0
            for line in order.order_line:
                if line.product_uom.name == "Nos":
                    qty_nos += line.product_uom_qty
            order.total_pur_qty_nos = qty_nos

    @api.depends('order_line.product_uom_qty')
    def _compute_pur_lit_quantity(self):
        for order in self:
            qty_ltr = 0
            for line in order.order_line:
                if line.product_uom.name == "L":
                    qty_ltr += line.product_uom_qty
            order.total_pur_qty_lit = qty_ltr

    @api.depends('order_line.product_uom_qty')
    def _compute_pur_unit_quantity(self):
        for order in self:
            qty_unit = 0
            for line in order.order_line:
                if line.product_uom.name == "Units":
                    qty_unit += line.product_uom_qty
            order.total_pur_qty_units = qty_unit



class InventoryQtyTotal(models.Model):
    _inherit = 'stock.picking'

    total_stk_qty_kg = fields.Float(string="Total Ordered Kg", compute='_compute_stk_kg_quantity', digits=0)
    total_stk_qty_nos = fields.Float(string="Total Ordered Nos", compute='_compute_stk_nos_quantity', digits=0)
    total_stk_qty_lit = fields.Float(string="Total Ordered Liter", compute='_compute_stk_lit_quantity', digits=0)
    total_stk_qty_units = fields.Float(string="Total Ordered Units", compute='_compute_stk_unit_quantity', digits=0)

    total_done_qty_kg = fields.Float(string="Total Ordered Kg", compute='_compute_done_kg_quantity', digits=0)
    total_done_qty_nos = fields.Float(string="Total Ordered Nos", compute='_compute_done_nos_quantity', digits=0)
    total_done_qty_lit = fields.Float(string="Total Ordered Liter", compute='_compute_done_lit_quantity', digits=0)
    total_done_qty_units = fields.Float(string="Total Ordered Units", compute='_compute_done_unit_quantity', digits=0)

    @api.depends('move_ids_without_package.quantity_done')
    def _compute_done_kg_quantity(self):
        for order in self:
            qty_kg = 0
            for line in order.move_ids_without_package:
                # unit = line.product_uom.name
                if line.product_uom.name == "kg":
                    qty_kg += line.quantity_done
                elif line.product_uom.name == "Kg":
                    qty_kg += line.quantity_done
            order.total_done_qty_kg = qty_kg

    @api.depends('move_ids_without_package.quantity_done')
    def _compute_done_nos_quantity(self):
        for order in self:
            qty_nos = 0
            for line in order.move_ids_without_package:
                if line.product_uom.name == "Nos":
                    qty_nos += line.quantity_done
            order.total_done_qty_nos = qty_nos

    @api.depends('move_ids_without_package.quantity_done')
    def _compute_done_lit_quantity(self):
        for order in self:
            qty_ltr = 0
            for line in order.move_ids_without_package:
                if line.product_uom.name == "L":
                    qty_ltr += line.quantity_done
            order.total_done_qty_lit = qty_ltr

    @api.depends('move_ids_without_package.quantity_done')
    def _compute_done_unit_quantity(self):
        for order in self:
            qty_unit = 0
            for line in order.move_ids_without_package:
                if line.product_uom.name == "Units":
                    qty_unit += line.quantity_done
            order.total_done_qty_units = qty_unit




    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_stk_kg_quantity(self):
        for order in self:
            qty_kg = 0
            for line in order.move_ids_without_package:
                # unit = line.product_uom.name
                if line.product_uom.name == "kg":
                    qty_kg += line.product_uom_qty
                elif line.product_uom.name == "Kg":
                    qty_kg += line.product_uom_qty
            order.total_stk_qty_kg = qty_kg

    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_stk_nos_quantity(self):
        for order in self:
            qty_nos = 0
            for line in order.move_ids_without_package:
                if line.product_uom.name == "Nos":
                    qty_nos += line.product_uom_qty
            order.total_stk_qty_nos = qty_nos

    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_stk_lit_quantity(self):
        for order in self:
            qty_ltr = 0
            for line in order.move_ids_without_package:
                if line.product_uom.name == "L":
                    qty_ltr += line.product_uom_qty
            order.total_stk_qty_lit = qty_ltr

    @api.depends('move_ids_without_package.product_uom_qty')
    def _compute_stk_unit_quantity(self):
        for order in self:
            qty_unit = 0
            for line in order.move_ids_without_package:
                if line.product_uom.name == "Units":
                    qty_unit += line.product_uom_qty
            order.total_stk_qty_units = qty_unit





class InvoiceQtyTotal(models.Model):
    _inherit = 'account.move'

    total_acc_qty_kg = fields.Float(string="Total Ordered Kg", compute='_compute_acc_kg_quantity', digits=0)
    total_acc_qty_nos = fields.Float(string="Total Ordered Nos", compute='_compute_acc_nos_quantity', digits=0)
    total_acc_qty_lit = fields.Float(string="Total Ordered Liter", compute='_compute_acc_lit_quantity', digits=0)
    total_acc_qty_units = fields.Float(string="Total Ordered Units", compute='_compute_acc_unit_quantity', digits=0)



    @api.depends('invoice_line_ids.quantity')
    def _compute_acc_kg_quantity(self):
        for order in self:
            qty_kg = 0
            for line in order.invoice_line_ids:
                # unit = line.product_uom.name
                if line.product_uom_id.name == "kg":
                    qty_kg += line.quantity
                elif line.product_uom_id.name == "Kg":
                    qty_kg += line.quantity
            order.total_acc_qty_kg = qty_kg

    @api.depends('invoice_line_ids.quantity')
    def _compute_acc_nos_quantity(self):
        for order in self:
            qty_nos = 0
            for line in order.invoice_line_ids:
                if line.product_uom_id.name == "Nos":
                    qty_nos += line.quantity
            order.total_acc_qty_nos = qty_nos

    @api.depends('invoice_line_ids.quantity')
    def _compute_acc_lit_quantity(self):
        for order in self:
            qty_ltr = 0
            for line in order.invoice_line_ids:
                if line.product_uom_id.name == "L":
                    qty_ltr += line.quantity
            order.total_acc_qty_lit = qty_ltr

    @api.depends('invoice_line_ids.quantity')
    def _compute_acc_unit_quantity(self):
        for order in self:
            qty_unit = 0
            for line in order.invoice_line_ids:
                if line.product_uom_id.name == "Units":
                    qty_unit += line.quantity
            order.total_acc_qty_units = qty_unit




