# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Location(models.Model):
    _inherit = 'stock.location'

    partner_id = fields.Many2one('res.partner', 'Address', default=lambda self: self.env.company.partner_id,
                                 check_company=True)
