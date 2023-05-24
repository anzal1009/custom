from odoo import models, fields, api,_


class SaleOrderMO(models.Model):
    _inherit = 'sale.order'

    def sales_mo(self):

        lines = []
        for item in self.order_line:

            product = item.product_id.name
            product_id = self.env['product.template'].sudo().search([('name', '=',product )]) or False
            print(product_id)

            vals = (0, 0, {
                'product':product_id.id,
                'qty': item.product_uom_qty,
            })
            lines.append(vals)
        return {'type': 'ir.actions.act_window',
                'name': _('MO Creation'),
                'res_model': 'sale.wizard',
                'target': 'new',
                'view_mode': 'form',
                'context': {'default_sale_wiz_line_idss': lines}
                }


