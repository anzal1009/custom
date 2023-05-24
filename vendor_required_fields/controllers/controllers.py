# -*- coding: utf-8 -*-
# from odoo import http


# class VendorRequiredFields(http.Controller):
#     @http.route('/vendor_required_fields/vendor_required_fields', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vendor_required_fields/vendor_required_fields/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vendor_required_fields.listing', {
#             'root': '/vendor_required_fields/vendor_required_fields',
#             'objects': http.request.env['vendor_required_fields.vendor_required_fields'].search([]),
#         })

#     @http.route('/vendor_required_fields/vendor_required_fields/objects/<model("vendor_required_fields.vendor_required_fields"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vendor_required_fields.object', {
#             'object': obj
#         })
