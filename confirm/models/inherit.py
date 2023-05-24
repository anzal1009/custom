from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ButtonInvInherit(models.Model):
    _inherit = "stock.move.line"

    carton_nos1 = fields.Float("CTN Number", tracking=True, store=True, force_save="1", readonly=True)
