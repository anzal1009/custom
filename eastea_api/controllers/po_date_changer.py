from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class poDateCorrection(http.Controller):
    @http.route('/5522668/change_po_date', type='json', csrf=False, auth='public')
    def poDateCorrection(self, **rec):
        # for rec in record["data"]:
        poNumber = rec["poNumber"]
        warehouse = rec["warehouse"]
        date1 = rec["date"]
        date = datetime.strptime(date1, '%d/%m/%Y')
        if (warehouse == 'JOTHIPURAM'):
            warehouse_data = warehouse and request.env['res.company'].sudo().search(
            [('name', '=', 'Eastea Chai Private Limited (Coimbatore)')], limit=1) or False
        if (warehouse == 'KAVALANGAD'):
            warehouse_data = warehouse and request.env['res.company'].sudo().search(
            [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
        purchase_order = request.env['purchase.order'].sudo().search(
            [('company_id', '=', warehouse_data.id),('name', '=', poNumber)])
        for purchase_order_1 in purchase_order:
            purchase_order_1.date_approve = date
            purchase_order_1.date_planned = date
            purchase_order_1.effective_date = date
            print(purchase_order_1)
            for po in purchase_order_1.picking_ids:
                print(po.date_done)
                if(po.date_done):
                    if(po.state != "done"):
                        po.scheduled_date = date
                    if(po.state == "done"):
                        # po.scheduled_date = date
                        po.date_done = date

    # def date_confirm(self):
    #     transfer = request.env['stock.picking'].sudo().search([('name', '=', self.name)])
    #
    #     for po in transfer:
    #         date = self.transaction_date
    #         po.date = date
    #         if (po.date_done):
    #             if(po.state != "done"):
    #                 po.scheduled_date = date
    #             if (po.state == "done"):
    #                 po.date_done = date
    #     for line_ids in po.move_line_ids:
    #         line_ids.date = date
    #         line_ids.move_id.date = date
