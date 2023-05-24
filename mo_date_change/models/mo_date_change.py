from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime
from odoo import api, models, fields, _


class MoDate(models.Model):
    _inherit = 'mrp.production'

    transaction_date = fields.Datetime(string="Production Date")

    # scheduled_date = fields.Datetime(readonly=0)

    def date_confirm(self):
        print("yess")
        mo = request.env['mrp.production'].sudo().search([('name', '=', self.name)])
        for po in mo:
            date = self.transaction_date
            # print(date)
            # po.date_planned_start = date
            # print(po)
        #     po.date = date
        #     if (po.date_done):
        #         if (po.state != "done"):
        #             po.scheduled_date = date
        #         if (po.state == "done"):
        #             po.date_done = date
        #     for line_ids in po.move_line_ids:
        #         line_ids.date = date
        #         line_ids.move_id.date = date
