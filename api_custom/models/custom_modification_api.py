from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from odoo import api, models, fields, _


class unlinkStockTransferRecord11(http.Controller):
    @http.route('/unlinkStockTransferRecord11', type='json', csrf=False, auth='public')
    def unlinkStockTransferRecord11(self, **rec):
        recordNumber = rec["recordNumber"]
        print(recordNumber)
        recordNumber = rec["recordNumber"]
        recordData = request.env['stock.picking'].sudo().search([('name', '=', recordNumber)]) or False
        for rec in recordData:
            rec.origin = False
            recordData = request.env['stock.move'].sudo().search([('picking_id', '=', rec.id)]) or False
            for i in recordData:
                i.picking_id = False


class PurchaseConfirmationDate(models.Model):
    _inherit = 'purchase.order'
    date_approve = fields.Datetime('Confirmation Date', readonly=0)


class TransferConfirmInventoryDate(models.Model):
    _inherit = 'stock.picking'
    date_done = fields.Datetime('Date of Transfer', readonly=0, )


class PoConfirm(http.Controller):
    @http.route('/po_confirm', type='json', csrf=False, auth='public')
    def po_confirm(self, **rec):
        for row in rec["data"]:
            ponumber = row["ponumber"]
            po = request.env['purchase.order'].sudo().search([('name', '=', ponumber)]) or False
            for rec in po:
                rec.button_confirm()
                rec.button_unlock()



