from odoo import models, fields, api,_


class ConfirmationDate(models.Model):
    _inherit = 'purchase.order'

    date_approve = fields.Datetime('Confirmation Date', readonly=0)



class ConfirmInventoryDate(models.Model):
    _inherit = 'stock.picking'

    date_done = fields.Datetime('Date of Transfer', readonly=0)
    scheduled_date = fields.Datetime('Scheduled Date',readonly=0)
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
        required=True, states={'confirmed': [('readonly', False)],'draft': [('readonly', False)],'assigned': [('readonly', False)],'done': [('readonly', False)]}, help="Location where the product you want to unbuild is.")

class ConfirmSaleDate(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime( readonly=0)





