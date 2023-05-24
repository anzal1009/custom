from odoo import http
from odoo.http import request

class BarcodeGenerator(http.Controller):
    @http.route('/data/barcode', type='json', auth='user')
    def barcode(self, **rec):

        for row in rec["data"]:
            reference = row["reference"]
            barcode = row["barcode"]

            product_id = reference and request.env['product.template'].sudo().search(
                [('default_code', '=', reference)], limit=1) or False
            # print(product_id.name)

            for b in product_id:
                b.barcode = barcode
