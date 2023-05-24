# -*- coding: utf-8 -*-
# from odoo import http


# class DefaultInvoicePrint(http.Controller):
#     @http.route('/default_invoice_print/default_invoice_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/default_invoice_print/default_invoice_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('default_invoice_print.listing', {
#             'root': '/default_invoice_print/default_invoice_print',
#             'objects': http.request.env['default_invoice_print.default_invoice_print'].search([]),
#         })

#     @http.route('/default_invoice_print/default_invoice_print/objects/<model("default_invoice_print.default_invoice_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('default_invoice_print.object', {
#             'object': obj
#         })
