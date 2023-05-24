from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    vehicle_no=fields.Char("Vehicle No.")
    dispatch_through=fields.Char("Dispatch Through")
    destination=fields.Char("Destination")
    dispatch_doc_no=fields.Char("Dispatch Doc No")
    other_ref=fields.Char("Ref")

    
class inventoryLocationCode(models.Model):
    _inherit = 'stock.location'

    loc_code=fields.Char("Location Code")
    loc_address = fields.Many2one("res.partner", string="Location Address", tracking=True)


class LocationCode(models.Model):
    _inherit = 'stock.picking'

    so_loc_code=fields.Char(string='Source Location Code',related='location_id.loc_code')
    dest_loc_code=fields.Char(string='Destination Location Code',related='location_dest_id.loc_code')



class LotNumberWeightForRM(models.Model):
    _inherit = "stock.production.lot"

    net_lot_weight = fields.Float("Net LOT Weight")
