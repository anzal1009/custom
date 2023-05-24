from odoo import fields, models, tools, api


class InventoryMovementReport(models.Model):
    _name = "stock.movement.report"
    _auto = False
    _description = "Inventory Movement Report"


    productname = fields.Char("Product Name")
    product_id = fields.Many2one("product.product","Product")
    category = fields.Many2one("product.category","Product Category")
    date = fields.Datetime('Date')
    internaltransfer = fields.Float("InternalTransfer")
    purchase = fields.Float("Purchase")
    sale = fields.Float("Sale")
    consumption = fields.Float("Consumption")
    manufacturing = fields.Float("Manufacturing")
    totaltransaction = fields.Float("TotalTransaction")


    # GROUP BY product_product.id ;
    def init(self):
        tools.drop_view_if_exists(self._cr, 'stock_movement_report')
        self._cr.execute("""
                CREATE OR REPLACE VIEW stock_movement_report AS
                (

                SELECT row_number() OVER ()                                                           AS id,
                       pdt_tmpl.name                                                                  as ProductName,
                       sm.create_date                                                                 as Date,
                       sm.product_id                                                                  as product_id,
                       pdt_tmpl.categ_id                                                              as Category,
                       SUM(sm.product_uom_qty)                                                        as TotalTransaction,
                       SUM(CASE WHEN spt.code = 'internal' THEN sm.product_uom_qty ELSE 0.0 END)      as InternalTransfer,
                       SUM(CASE WHEN spt.code = 'incoming' THEN sm.product_uom_qty ELSE 0.0 END)      as Purchase,
                       SUM(CASE WHEN spt.code = 'outgoing' THEN sm.product_uom_qty ELSE 0.0 END)      as Sale,
                       SUM(CASE WHEN (spt.code = 'mrp_operation' AND sm.production_id > 0) THEN sm.product_uom_qty ELSE 0.0 END) as Manufacturing,
                       SUM(CASE WHEN (spt.code = 'mrp_operation' AND sm.raw_material_production_id > 0) THEN sm.product_uom_qty ELSE 0.0 END) as Consumption
                FROM stock_move sm
                         LEFT JOIN stock_picking_type spt ON sm.picking_type_id = spt.id
                         LEFT JOIN product_product pdt ON sm.product_id = pdt.id
                         LEFT JOIN product_template pdt_tmpl ON pdt.product_tmpl_id = pdt_tmpl.id
                GROUP BY pdt_tmpl.name, sm.create_date,pdt_tmpl.categ_id,sm.product_id 


                )""")
