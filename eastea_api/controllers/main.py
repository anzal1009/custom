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

    # **************************2234234*****************************************************


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


# ******************Purchase*****************
class PurchaseOrder(models.Model):
    name = "purchase.order"



    def purchase_order(self):

    
        if not new_invoice:
            raise UserError(_('There is an error Please check your server'))
        for row in new_invoice:
            vals = {}
            purchase_order = self.env['purchase.order'].sudo().search([('order_id', '=', row.partner_reference)], limit=1)
            partner_id = row.vat and self.env['res.partner'].sudo().search([('GSTIN', '=', row.vat)], limit=1).id or False
        if not partner_id:
            raise UserError(_('There is an error Please check your server'))
        for row in partner_id:
                vendor_details = {
                    'name': row[1],
                    'currency_id': 20,
                    'street': row[3],
                    'street2': " ",
                    'city': " ",
                    'zip': " ",
                    'phone': " ",
                    'email': " ",
                    'vat': row[4],
                    'parent_id': 1
                }
        partner_id=self.env['res.partner'].sudo().create({'name': 'row.Vendor_name'})
        self.env.cr.commit()


            # print(row.SALES_ORDER_NUMBER)
            # exit()




            


        if not purchase_order:
                order_line=[]
                for row in invoice:
                    invoice_date = row.TRANSACTION_DATE
                    product_id = self.env['product.product'].sudo().search([('name', '=', row.ITEM_DESC)], limit=1) or False


                    if not product_id:
                        uom_ids=self.env['uom.uom'].sudo().search([])
                        unit_id=self.env.ref('uom.product_uom_unit') and self.env.ref('uom.product_uom_unit').id or False
                        for record in uom_ids:
                            if record.name.upper() ==row.TRANSACTION_UOM.upper():
                                unit_id=record.id
                                break



                        try:
                            product_line_dict = {

                                            'name': row.ITEM_DESC,
                                            'default_code': row.ITEM_NUM,
                                            'list_price': row.UNIT_PRICE,
                                            'l10n_in_hsn_code': row.HSN_CODE,
                                            # 'uom_id': unit_id,
                                            # 'uom_po_id': unit_id,
                                            'detailed_type': 'product',
                                            'categ_id': 1,
                                            'standard_price': row.UNIT_PRICE
                                        }
                        except:
                            raise UserError(_('Please verify the purchase invoice '+' '+ row.INVOICE_NUM +' for item '+ row.ITEM_DESC))
                        product_id = self.env['product.template'].sudo().create(product_line_dict)
                        self.env.cr.commit()




                    if product_id:
                        if product_id.categ_id:
                            categ_id=product_id.categ_id
                            if categ_id.property_cost_method != 'avarage' and categ_id.property_valuation != 'real_time':
                                raise UserError(_('Please Configure Product Category Values (Costing Method and Inventory Valuation'))
                        # tax_percent = str(float(row.CGST + row.SGST))
                        tax_domain = [('amount', '=', str(int(float(row.CGST + row.SGST)))), ('type_tax_use', '=','purchase'),
                             ('name', '=', "GST "+str(int(float(row.CGST + row.SGST)))+"%")]
                        if self.env.company:
                            tax_domain.append(('company_id', '=', self.env.company.id))
                        tax_variant = self.env['account.tax'].search(tax_domain, limit=1)
                        if (row.CGST or row.SGST) and not tax_variant:
                            raise UserError(_('Please Configure Tax '+str(row.CGST)+','+str(row.SGST)))
                       


                        

                        order_line.append((0, 0, {
                            'display_type': False,
                                             # 'sequence': 10,
                                             'product_id': product_id.id,
                                             'name': product_id.name or '',
                                             'date_planned': row.TRANSACTION_DATE or False,
                                             'account_analytic_id': False,
                                             'product_qty': row.PRIMARY_QUANTITY or 0,
                                             'qty_received_manual': 0,
                                             'product_uom': product_id.uom_id.id or self.env.ref('uom.product_uom_unit') and self.env.ref('uom.product_uom_unit').id or False,
                                             'price_unit': row.UNIT_PRICE or 0,
                                             'taxes_id': tax_variant and [(6, 0, [tax_variant.id])] or [],
                        }))


                   

                   
                    
                if partner_id:
                        purchase_order_1 = False
                        # try:
                        purchase_order_1 = self.env['purchase.order'].create({
                                'partner_id': partner_id,
                                'partner_ref': row.order_id or '',
                                'origin': row.order_id or '',
                                'date_order': row.TRANSACTION_DATE or False,
                                'date_approve': row.TRANSACTION_DATE or False,
                                #'partner_id': self.env.ref('base.main_partner').id,
                                'name':row.INVOICE_NUM or '',
                                'order_line':order_line,
                            })

                        self.env.cr.commit()











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
