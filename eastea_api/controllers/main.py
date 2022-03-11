from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import datetime


class Purchase(http.Controller):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/get_products', type='json', auth='user')
    def get_products(self):
        print("Yes here entered")
        patients_rec = request.env['product.template'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                # 'id': rec.partner_id,
                'name': rec.name,
                'qty': rec.qty_available,
                'loc': rec.property_stock_inventory.name,
                'id': rec.company_id,
            }
            patients.append(vals)
        print("Purchase order--->", patients)
        data = {'status': 200, 'response': patients, 'message': 'Done All Products Returned'}
        return data

    # *******************************************************************************


    #
    # @http.route('/create_purchase', type='json', auth='user')
    # def create_purchase(self, **rec):
    #     if request.jsonrequest:
    #         # print("rec", rec)
    #         if rec['vendor']:
    #             vals = {
    #
    #                 'partner_id': rec['vendor'],
    #                 # 'name': rec['name'],
    #                 # 'product_id':rec['product']
    #                 # 'photo': rec['photo']
    #             }
    #
    #             new_customer = request.env['purchase.order'].sudo().create(vals)
    #             print("New Customer Is", new_customer)
    #             args = {'success': True, 'message': 'Success', 'id': new_customer.id}
    #     return args

    @http.route('/action_approve', type='json', auth='user')
    def action_approve(self):
        for record in self:
            pick_lines = []
            for line in record.request_line_ids:
                pick_line_values = {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.issued_product_qty,
                    'product_uom': line.product_id.uom_id.id,
                    'state': 'draft',
                }
                pick_lines.append((0, 0, pick_line_values))
            picking = {
                'location_id':record.location_id ,
                'location_dest_id': record.location_dest_id.id,
                'move_type': 'direct',
                'picking_type_id': record.picking_type_id,
                'ctsrf': record.id,
                'move_lines': pick_lines,
            }
            transfer = self.env['stock.picking'].sudo().create(picking)
            if transfer:
                record.state = 'approved'
                record.approved_date = datetime.Datetime.now()
                record.approved_by = self.env.uid
            else:
                raise ValidationError(("Something went wrong during your Request generation"))
        return True












    # def action_approve(self, **rec):
    #     if request.jsonrequest:
    #         print("rec", rec)
    #         if rec['location_dest_id']:
    #             for record in self:
    #                 pick_lines = []
    #         for line in record.request_line_ids:
    #             pick_line_values = {
    #                 'product_id': line.product_id,
    #                 'name': line.product_id.name,
    #                 'qty': line.product_uom_qty,
    #                 'uom': line.product_uom,
    #                 'state': 'draft',
    #             }
    #             pick_lines.append((0, 0, pick_line_values))
    #         picking = {
    #             'location_id': 8,
    #             'location_dest_id': record.location_dest_id,
    #             'move_type': 'direct',
    #             'picking_type_id': 5,
    #             'ctsrf': record.id,
    #             'move_ids_without_package': pick_lines,
    #         }
    #         transfer = self.env['stock.picking'].sudo().create(picking)
    #         if transfer:
    #             record.state = 'approved'
    #             record.approved_date = date.Datetime.now()
    #             record.approved_by = self.env.uid
    #         else:
    #             raise
    #
    #             # raise ValidationError(("Something went wrong during your Request generation"))
    #
    #     return True
