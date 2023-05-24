from odoo.exceptions import ValidationError
from datetime import datetime
from odoo import api, models, fields, _


class StockField(models.Model):
    _inherit = 'stock.quant'

    cmmt = fields.Char(string="Comments")

    # @api.model
    # def _get_inventory_fields_write(self):
    #
    #     """ Returns a list of fields user can edit when he want to edit a quant in `inventory_mode`.
    #     """
    #     fields = ['inventory_quantity', 'inventory_quantity_auto_apply', 'inventory_diff_quantity',
    #               'inventory_date', 'user_id', 'inventory_quantity_set', 'is_outdated', 'cmmt']
    #     return fields

        # res = super(StockField, self)._get_inventory_fields_write()
        # return res


    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        return ['product_id', 'location_id', 'lot_id', 'package_id', 'owner_id', 'cmmt'] + self._get_inventory_fields_write()
        # res = super(StockField, self)._get_inventory_fields_create()
        # return res