# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def create(self, values):
        if self.env.user.has_group('restrict_bom_creation.group_bom_creation'):
            raise UserError(_('You are not allowed to create/ edit BOM. Please contact Administrator.'))

        return super(MrpBom, self).create(values)

    def write(self, values):
        if self.env.user.has_group('restrict_bom_creation.group_bom_creation'):
            raise UserError(_('You are not allowed to create/ edit BOM. Please contact Administrator.'))

        return super(MrpBom, self).write(values)

    def unlink(self):
        if self.env.user.has_group('restrict_bom_creation.group_bom_creation'):
            raise UserError(_('You are not allowed to delete this BOM. Please contact Administrator.'))
        else:
            return super(MrpBom, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('restrict_bom_creation.group_bom_creation'):
                raise UserError(_('You can not archive/ unarchive this bom. Please contact Administrator.'))
            return super(MrpBom, order).toggle_active()

