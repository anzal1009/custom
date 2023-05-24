# -*- coding: utf-8 -*-
# from odoo import http


# class InvSequenceWh(http.Controller):
#     @http.route('/inv_sequence_wh/inv_sequence_wh', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inv_sequence_wh/inv_sequence_wh/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inv_sequence_wh.listing', {
#             'root': '/inv_sequence_wh/inv_sequence_wh',
#             'objects': http.request.env['inv_sequence_wh.inv_sequence_wh'].search([]),
#         })

#     @http.route('/inv_sequence_wh/inv_sequence_wh/objects/<model("inv_sequence_wh.inv_sequence_wh"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inv_sequence_wh.object', {
#             'object': obj
#         })
