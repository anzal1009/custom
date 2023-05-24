from odoo import models, fields, api


class ManufactureOrder(models.Model):
    _inherit = 'account.asset'

    assets_type = fields.Char("Assets Type")
    assets_grp =fields.Selection([('l', 'Land'), ('b', 'Factory Building'), ('f', 'Furniture and Fixtures'),('e', 'Electrical Equipments'),('le', 'Lab Equipments'),
    ('o', 'Office Equipments') , ('in', 'Intangible Asset'),('lcm', 'Light Commercial Motor Vehicle'),('lm', 'Light Motor Vehicle'),('vh', 'Vehicle'),('com', 'Computer & Peripherals'),
                                  ('feq', 'Factory Equipment'),('pm', 'Plant and Machinery')], string='Assets Group')
    assets_qty =fields.Char("Assets Units")
    assets_no =fields.Char("Assets No")
    assets_dtls=fields.Char("Assets Details")
    assets_loc=fields.Char("Assets Location")
    assets_dept=fields.Char("Assets Department")
