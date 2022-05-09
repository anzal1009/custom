from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    vehicle_no=fields.Char("Vehicle No.")
    dispatch_through=fields.Char("Dispatch Through")
    destination=fields.Char("Destination")
    dispatch_doc_no=fields.Char("Dispatch Doc No")
    # other_ref=fields.Char("Ref")

