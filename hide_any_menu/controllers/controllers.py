# -*- coding: utf-8 -*-
# from odoo import http


# class HideAnyMenu(http.Controller):
#     @http.route('/hide_any_menu/hide_any_menu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hide_any_menu/hide_any_menu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hide_any_menu.listing', {
#             'root': '/hide_any_menu/hide_any_menu',
#             'objects': http.request.env['hide_any_menu.hide_any_menu'].search([]),
#         })

#     @http.route('/hide_any_menu/hide_any_menu/objects/<model("hide_any_menu.hide_any_menu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hide_any_menu.object', {
#             'object': obj
#         })
