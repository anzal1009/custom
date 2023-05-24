from odoo import models, fields, api, _, tools
from time import strftime
from odoo.http import request
from datetime import date

import datetime


# class ExportSaleInvoiceReport(models.Model):
#     _inherit = "account.move.line"
    
#     qty_in_ctn = fields.Float("QTY in CTN")

class SaleDeliveryReport(models.Model):
    _inherit = "sale.order.line"

    mo_date = fields.Date("MFG Date")
    pack = fields.Char("Pack Numbers")
    qtyp = fields.Float("QTY in Pkg")
    pkts = fields.Char(related='product_id.pkt_ctn',string="Pkts/CTN")
    net = fields.Char(related='product_id.net_ctn',string="Net Wt/CTN")
    total_net = fields.Char( string= "Total Net Wt in KGS", compute='onchange_compute_total_net')
    grs = fields.Char(related='product_id.gross_ctn',string="Gross Wt/CTN")
    total_grs = fields.Float("Total GRS Wt in KGS", compute='onchange_compute_total_grs')
    batch = fields.Char("Batch No")
    exp = fields.Date("EXP date", compute='_compute_exp_date')
    
    vol = fields.Float(string="Volume",related='product_id.volume')
    line_cbm = fields.Float(string="Pdt Cbm")

    @api.onchange('qtyp')
    def onchange_compute_line_cbm(self):
    # def compute_compute_pdt_cbm(self):
        for line in self:
            line.line_cbm = round(float(line.qtyp) * float(line.vol), 2)


#     @api.onchange('qtyp')
    def onchange_compute_total_net(self):
        for line in self:
            line.total_net = round(float(line.net) * float(line.qtyp),2)

#     @api.onchange('qtyp')
    def onchange_compute_total_grs(self):
        for line in self:
            line.total_grs = round(float(line.grs) * float(line.qtyp),2)

    def _compute_exp_date(self):
        for line in self:
            creation_date = line.mo_date
            if creation_date:
                new_date = (creation_date + datetime.timedelta(days=2 * 350)).strftime('%Y-%m-%d')
                line.exp = new_date
            else:
                line.exp = False







class ItemMasterInherit(models.Model):
    _inherit = "product.template"

    pkt_ctn = fields.Char("Pkts/ CTN")
    net_ctn = fields.Char("Net Wt/ CTN")
    gross_ctn = fields.Char("Gross Wt/ CTN")
    
    

class LotNumberDate(models.Model):
    _inherit = "stock.production.lot"

    dated = fields.Date(compute='onchange_compute_date',string="Date")

    # @api.onchange('product_id')
    def onchange_compute_date(self):
        for lot in self:
            creation_date = lot.create_date
            new_date = (creation_date + datetime.timedelta(days=2 * 350)).strftime('%Y-%m-%d')
            lot.dated = new_date






