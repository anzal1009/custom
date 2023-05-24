from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class TyreManagement(models.Model):
    _name = 'tyre.management'

    name = fields.Char("Name")
    custom_id = fields.Char("Custom id")


    def button_inventory(self):
        print("hgd")