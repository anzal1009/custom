from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from odoo import api, models, fields, _


class DateTransfers(models.Model):
    _inherit = 'stock.picking'

    transaction_date = fields.Datetime(string="Transaction Date")

    # scheduled_date = fields.Datetime(readonly=0)

    def date_confirm(self):
        transfer = request.env['stock.picking'].sudo().search([('name', '=', self.name)])
        for po in transfer:
            date = self.transaction_date
            po.date = date
            if (po.date_done):
                if (po.state != "done"):
                    po.scheduled_date = date
                if (po.state == "done"):
                    po.date_done = date
            for line_ids in po.move_line_ids:
                line_ids.date = date
                line_ids.move_id.date = date
