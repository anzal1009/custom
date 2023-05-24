from odoo import models,fields,api



class ButtonChckInherit(models.Model):
    _inherit = "stock.picking"

    mo_transfer = fields.Boolean(
        compute='_compute_mo_transfer',string="Mo Transfer")


    @api.depends('origin')
    def _compute_mo_transfer(self):
        print("hh")
        for pick in self:
            if pick.origin:
                source = pick.origin
                if source.startswith('KV/BLD'):
                    pick.mo_transfer = True
                else:
                    pick.mo_transfer = False
            else:
                pick.mo_transfer = False
