from odoo import http
from odoo.http import request


class Medical(http.Controller):

    @http.route('/medical_store/products', auth='public', website=True)
    def medical_products(self):
        # return "haii"

        # products = request.env['medical.products'].sudo().search([])
        return request.render("medical_store.medical_products", {'products': products})

# #
# class Medical(http.Controller):
#
#     @http.route('/product_webform', type="http", auth="public", website=True)
#     def product_webform(self, **kw):
#
#         print("Execution Here.........................")
        # doctor_rec = request.env['hospital.doctor'].sudo().search([])
        # print("doctor_rec...", doctor_rec)
        # return http.request.render('medical_store.create_product', {})
#
#     @http.route('/create/webproduct', type="http", auth="public", website=True)
#     def create_webproducts(self, **kw):
#         # print("Data Received.....", kw)
#         request.env['medical.products'].sudo().create(kw)
#         # doctor_val = {
#         #     'name': kw.get('patient_name')
#         # }
#         # request.env['hospital.doctor'].sudo().create(doctor_val)
#         return request.render("medical_store.product_thanks", {})
