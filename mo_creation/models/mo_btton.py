# import requests as requests

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError, UserError
from odoo import exceptions
import collections
from odoo import tools
import requests
import  json


class MoButtonApi(models.Model):
    _inherit = 'mrp.production'



    def action_mo_details(self):
        print("yesss")
    #
    # def button_mark_done(self):
    #     res = super(MoButtonApi, self).button_mark_done()
    #
    #     print("complt")
    #     return res
        # def ConfirmMODetails(self):
        moName = self.name
        mo_rec = self.env['mrp.production'].sudo().search([('name', '=', moName)])
        mo_details = []
        for rec in mo_rec:
            order_lines = []
            for line in rec.move_raw_ids:
                for l in line.move_line_ids:
                    order_lines.append({
                        'consumed_product': l.product_id.name,
                        'quantity': l.qty_done,
                        'batch_no': l.lot_id.name,
                        # 'done_qty':line.quantity_done
                    })
            vals = {
                # 'id': rec.partner_id,
                'mo_number': moName,
                'status': "COMP LETED",
                #                 'qty': rec.product_qty,
                #                 'blend': rec.blend,
                # 'bom_id':rec.b,om_id.id,
                #                 'date': rec.date_planned_start,
                'child': order_lines,
            }
            print(vals)
        #             mo_details.append(vals)
        #         data = {'status': 200, 'response': mo_details}
        #         return vals
        if vals:
            url = "http://192.168.29.226:3000/mo/mo-usage"
            headers = {"Content-type": "application/json"}

            try:
                # print("hiii")
                req = requests.post(url, data=json.dumps(vals), headers=headers, timeout=50)
                req.raise_for_status()
                print(req)

                content = req.json()

                print(content )

            # if content['status'] == '201':
            except requests.exceptions.HTTPError as err:
                print('err',err.response.json()['message'])


                error_msg = _(err.response.json()['message'])
                raise self.env['res.config.settings'].get_config_warning(error_msg)