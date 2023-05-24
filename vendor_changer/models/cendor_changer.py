from odoo import models, fields, api,_
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger




class PurchaseVendor(models.Model):
    _inherit = 'purchase.order'

def action_changer(self):
    print("ffd")