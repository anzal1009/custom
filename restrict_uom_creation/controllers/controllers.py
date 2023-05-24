# -*- coding: utf-8 -*-
# from odoo import http


# class RestrictUomCreation(http.Controller):
#     @http.route('/restrict_uom_creation/restrict_uom_creation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrict_uom_creation/restrict_uom_creation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrict_uom_creation.listing', {
#             'root': '/restrict_uom_creation/restrict_uom_creation',
#             'objects': http.request.env['restrict_uom_creation.restrict_uom_creation'].search([]),
#         })

#     @http.route('/restrict_uom_creation/restrict_uom_creation/objects/<model("restrict_uom_creation.restrict_uom_creation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrict_uom_creation.object', {
#             'object': obj
#         })
