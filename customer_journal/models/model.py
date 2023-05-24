from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomerJournal(models.Model):
    _inherit = "res.partner"

    # jornal_id =