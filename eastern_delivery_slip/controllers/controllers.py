# -*- coding: utf-8 -*-
# from odoo import http


# class EasternDeliverySlip(http.Controller):
#     @http.route('/eastern_delivery_slip/eastern_delivery_slip', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eastern_delivery_slip/eastern_delivery_slip/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eastern_delivery_slip.listing', {
#             'root': '/eastern_delivery_slip/eastern_delivery_slip',
#             'objects': http.request.env['eastern_delivery_slip.eastern_delivery_slip'].search([]),
#         })

#     @http.route('/eastern_delivery_slip/eastern_delivery_slip/objects/<model("eastern_delivery_slip.eastern_delivery_slip"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eastern_delivery_slip.object', {
#             'object': obj
#         })
