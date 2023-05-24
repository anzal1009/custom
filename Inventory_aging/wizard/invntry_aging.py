from odoo import models, fields, api, _


class InventoryWizard(models.TransientModel):
    _name = "inventory.wizard"

    name = fields.Date("Date")
