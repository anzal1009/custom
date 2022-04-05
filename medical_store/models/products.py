import qrcode
import base64
from io import BytesIO

from odoo import api,models, fields, _


class MedicalShop(models.Model):
        _name = "medical.products"

        name = fields.Char(string='Product Name')
        name_seq = fields.Char(string='Product ID', required=True, copy=False, readonly=True,
                               default=lambda self: _('New'))

        proid = fields.Char(string='Product Price')
        qr_code = fields.Binary("QR Code", attachment=True, store=True)
        category = fields.Selection([('t', 'Tablet'), ('s', 'Syrup'), ('o', 'oilment')], string='Category')
        note = fields.Text(string='Description', tracking=True)

        @api.model
        def create(self, vals):
                # if not vals.get('note'):
                #         vals['note'] = 'New Patient'

                if vals.get('name_seq', _('New')) == _('New'):
                         vals['name_seq'] = self.env['ir.sequence'].next_by_code('medical.products') or _('New')
                res = super(MedicalShop, self).create(vals)
                return res

        @api.onchange('note')
        def generate_qr_code(self):
                qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                )
                qr.add_data(self.note)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                self.qr_code = qr_image
