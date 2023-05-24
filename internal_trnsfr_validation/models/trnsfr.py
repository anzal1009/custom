from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TransferGrn(models.Model):
    _inherit = "stock.location"

    loc_incharge = fields.Many2one("res.users",string="In Charge",tracking=True)



class PickingValidate(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        if self.picking_type_id.code =='internal':
            if self.location_dest_id:
                loc =self.location_dest_id

                #
                # print("location user",loc.loc_incharge.name)
                # print("user",self.user_id.name)
                # print("Login user",self.env.user.name)
                loc_user = loc.loc_incharge

                if loc.loc_incharge:

                    if self.env.user == loc_user:
                        res = super(PickingValidate, self).button_validate()
                        return res
                    else:
                        raise ValidationError("Please Verify Transfer with Location Incharge")
                else:
                    res = super(PickingValidate, self).button_validate()
                    return res
        else:
            res = super(PickingValidate, self).button_validate()
            return res
