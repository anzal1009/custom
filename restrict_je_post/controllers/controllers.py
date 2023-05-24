# -*- coding: utf-8 -*-
# from odoo import http


# class RestrictJePost(http.Controller):
#     @http.route('/restrict_je_post/restrict_je_post', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/restrict_je_post/restrict_je_post/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('restrict_je_post.listing', {
#             'root': '/restrict_je_post/restrict_je_post',
#             'objects': http.request.env['restrict_je_post.restrict_je_post'].search([]),
#         })

#     @http.route('/restrict_je_post/restrict_je_post/objects/<model("restrict_je_post.restrict_je_post"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('restrict_je_post.object', {
#             'object': obj
#         })
