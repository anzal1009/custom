# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, values):
        if self.env.user.has_group('restrict_product_creation.group_product_creation'):
            raise UserError(_('You are not allowed to create/ edit product. Please contact Administrator.'))

        return super(ProductTemplate, self).create(values)

    def unlink(self):
        if self.env.user.has_group('restrict_product_creation.group_product_creation'):
            raise UserError(_('You are not allowed to delete this product. Please contact Administrator.'))
        else:
            return super(ProductTemplate, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('restrict_product_creation.group_product_creation'):
                raise UserError(_('You can not archive/ unarchive this product. Please contact Administrator.'))
            return super(ProductTemplate, order).toggle_active()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, values):
        if self.env.user.has_group('restrict_product_creation.group_product_creation'):
            raise UserError(_('You are not allowed to create/ edit product. Please contact Administrator.'))
        return super(ProductProduct, self).create(values)

    def unlink(self):
        if self.env.user.has_group('restrict_product_creation.group_product_creation'):
            raise UserError(_('You are not allowed to delete this product. Please contact Administrator.'))
        else:
            return super(ProductProduct, self).unlink()

    def toggle_active(self):
        for order in self:
            if self.env.user.has_group('restrict_product_creation.group_product_creation'):
                raise UserError(_('You can not archive/ unarchive this product. Please contact Administrator.'))
            return super(ProductProduct, order).toggle_active()
