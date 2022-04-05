from odoo import api,models, fields,_

class MedicalShop(models.Model):
        _name = "medical.staff"


        name = fields.Char(string='Staff Name')
        # staffid = fields.Char(string='Staff Id')
        phone = fields.Char(string='Mobile No')
        saddres = fields.Char(string='Address')
        sales_count = fields.Integer(string='Sales Count', compute='_compute_sales_count')

        name_seq = fields.Char(string='Employee ID', required=True, copy=False, readonly=True,default=lambda self: _('New'))

        def _compute_sales_count(self):
                sales_count = self.env['medical.sales'].search_count([('name', '=', self.id)])
                self.sales_count = sales_count

        def action_open_sales(self):
                return {
                        'name': _('Sales'),
                        'domain': [('name', '=', self.id)],
                        'res_model': 'medical.sales',
                        'view_id': False,
                        'view_mode': 'tree,form',
                        'type': 'ir.actions.act_window',
                }

        @api.model
        def create(self, vals):
                # if not vals.get('note'):
                #         vals['note'] = 'New Patient'

                if vals.get('name_seq', _('New')) == _('New'):
                        vals['name_seq'] = self.env['ir.sequence'].next_by_code('medical.staff') or _('New')
                res = super(MedicalShop, self).create(vals)
                return res




