from odoo import api,models, fields,_


class SaleOrderInherit(models.Model):
    _inherit = 'account.move'



    def action_print_sale_invoice(self):
        return self.env.ref('eastea - custom.sale_order_report_receipt1').report_action(self)


    def action_print_purchase_invoice(self):
        return self.env.ref('eastea-custom.purchase_order_report_qweb_paperform1').report_action(self)