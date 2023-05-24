# -*- coding: utf-8 -*-
# from odoo import http


# class RestrictBomCreation(http.Controller):
#     @http.route('/restrict_bom_creation/restrict_bom_creation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrict_bom_creation/restrict_bom_creation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrict_bom_creation.listing', {
#             'root': '/restrict_bom_creation/restrict_bom_creation',
#             'objects': http.request.env['restrict_bom_creation.restrict_bom_creation'].search([]),
#         })

#     @http.route('/restrict_bom_creation/restrict_bom_creation/objects/<model("restrict_bom_creation.restrict_bom_creation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrict_bom_creation.object', {
#             'object': obj
#         })
