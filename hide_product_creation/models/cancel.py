from odoo import models, fields, api
from odoo.exceptions import ValidationError

######################### Sale ################################


class SaleCancelButton(models.Model):
    _inherit = "sale.order"

    # def action_transfr(self):
    #     print("yess")

    
