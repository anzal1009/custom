from odoo import models, fields, api, _, tools
from odoo.http import request


class ScaDelivery(models.Model):

    _inherit = "stock.picking"



    @api.onchange('location_id')
    def onchange_product_id(self):
        if self.location_id:
            address=  request.env['res.company'].sudo().search([])
            for add in address:
                add.company_details = self.location_id.address.name


