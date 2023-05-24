# -*- coding: utf-8 -*-
# from odoo import http


# class UniquePartnerCode(http.Controller):
#     @http.route('/unique_partner_code/unique_partner_code', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unique_partner_code/unique_partner_code/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('unique_partner_code.listing', {
#             'root': '/unique_partner_code/unique_partner_code',
#             'objects': http.request.env['unique_partner_code.unique_partner_code'].search([]),
#         })

#     @http.route('/unique_partner_code/unique_partner_code/objects/<model("unique_partner_code.unique_partner_code"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unique_partner_code.object', {
#             'object': obj
#         })
