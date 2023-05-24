# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class UoM(models.Model):
    _inherit = 'uom.uom'

    @api.model
    def create(self, values):
        if self.env.user.has_group('restrict_uom_creation.group_hide_uom_creation'):
            raise UserError(_('You are not allowed to create UoM. Please contact Administrator.'))
        return super(UoM, self).create(values)

    def write(self, values):
        if self.env.user.has_group('restrict_uom_creation.group_hide_uom_creation'):
            raise UserError(_('You are not allowed to edit this UoM. Please contact Administrator.'))
        return super(UoM, self).write(values)

    def unlink(self):
        if self.env.user.has_group('restrict_uom_creation.group_hide_uom_creation'):
            raise UserError(_('You are not allowed to delete this UoM. Please contact Administrator.'))
        else:
            return super(UoM, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('restrict_uom_creation.group_hide_uom_creation'):
                raise UserError(_('You can not archive/ unarchive this UoM. Please contact Administrator.'))
            return super(UoM, order).toggle_active()
