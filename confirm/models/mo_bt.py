from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ButtonMoInherit(models.Model):
    _inherit = "mrp.production"


    cost_comp = fields.Boolean("Compute Cost" ,readonly =True, default=True)

    def button_compute(self):
        print("yess")
        for line in self:
            line.cost_comp =True
