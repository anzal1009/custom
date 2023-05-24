# -*- coding: utf-8 -*-
# from odoo import http


# class IsCustomerVendor(http.Controller):
#     @http.route('/is_customer_vendor/is_customer_vendor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/is_customer_vendor/is_customer_vendor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('is_customer_vendor.listing', {
#             'root': '/is_customer_vendor/is_customer_vendor',
#             'objects': http.request.env['is_customer_vendor.is_customer_vendor'].search([]),
#         })

#     @http.route('/is_customer_vendor/is_customer_vendor/objects/<model("is_customer_vendor.is_customer_vendor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('is_customer_vendor.object', {
#             'object': obj
#         })
