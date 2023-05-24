# -*- coding: utf-8 -*-
# from odoo import http


# class SaleConfirmationDate(http.Controller):
#     @http.route('/sale_confirmation_date/sale_confirmation_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_confirmation_date/sale_confirmation_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_confirmation_date.listing', {
#             'root': '/sale_confirmation_date/sale_confirmation_date',
#             'objects': http.request.env['sale_confirmation_date.sale_confirmation_date'].search([]),
#         })

#     @http.route('/sale_confirmation_date/sale_confirmation_date/objects/<model("sale_confirmation_date.sale_confirmation_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_confirmation_date.object', {
#             'object': obj
#         })
