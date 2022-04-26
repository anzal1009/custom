from odoo import api,models, fields,_


class SaleOrderInherit(models.Model):
    _inherit = 'account.move'

    # ************** Print report button ******************

    def action_print_sale_invoice(self):
        return self.env.ref('eastea-custom.sale_order_report_qweb_paperform1').report_action(self)


    def action_print_purchase_invoice(self):
        return self.env.ref('eastea-custom.purchase_order_report_qweb_paperform1').report_action(self)


#**************************************************************

    # def action_generate_irn(self):
    #     print('hello')
    #     # return self.env.ref('eastea-custom.purchase_order_report_qweb_paperform1').report_action(self)



# class SaleOrderInherit1(models.Model):
#     _inherit = 'sale.order'

#     def action_quotation_send(self):
#         print('yyy')
