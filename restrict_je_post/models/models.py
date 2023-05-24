# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        if self.move_type =="entry":
            if not self.env.user.has_group('restrict_je_post.group_je_posting'):
                raise UserError(_('You are not allowed to post this Journal Entry. Please contact Administrator.'))

        return super(AccountMove, self).action_post()

