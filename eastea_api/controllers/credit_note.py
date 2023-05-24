from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _
from time import time

class CreditNote(http.Controller):

    @http.route('/data/credit_note', type='json', auth='user')
    def credit_note_creation(self, **rec):
        credit_note_no=[]
        for row in rec["data"]:
            is_gst = row["child"][0]["cgst"]
            if is_gst:
                vendor_name = "Route IntraState Sales"
            is_igst = row["child"][0]["igst"]
            if is_igst:
                vendor_name= "Route InterState Sales"

            invoice_date = row["master"]["bill_date"]
            date = datetime.strptime(invoice_date, '%d/%m/%Y')

            sale_to_company = row["master"]["company_ware_house"]["name"]
            if (sale_to_company == 'JOTHIPURAM'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (TN)')], limit=1) or False
            if (sale_to_company == 'KAVALANGAD'):
                to_company_detail2 = sale_to_company and request.env['res.company'].sudo().search(
                    [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

            jounalname = "Route Sale"
            jounal_id = jounalname and request.env['account.journal'].sudo().search(
                [('name', '=', jounalname), ('company_id', '=', to_company_detail2.id)], limit=1) or False

            # vendor_gst = row["master"]["partner_id"]["gst_no"]
            if vendor_name:
                vendor = vendor_name and request.env['res.partner'].sudo().search([('name', '=', vendor_name)],
                                                                                 limit=1) or False

                if not vendor:
                    raise ValidationError(_("Route not found"))



                invoice_line_ids = []
                for line in row["child"]:
                    product = line["product"]
                    quantity = line["quantity"]
                    price = line["price_unit"]
                    # tax =line["tax"]
                    gst = line["cgst"] + line["sgst"]
                    igst = line["igst"]
                    tax_variant = False
                    if gst:
                        tax_variant = request.env['account.tax'].sudo().search(
                            [('company_id', '=', to_company_detail2.id), ('amount', '=', str(gst)),
                             ('type_tax_use', '=', "purchase"),
                             ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                    if igst:
                        tax_variant = request.env['account.tax'].sudo().search(
                            [('company_id', '=', to_company_detail2.id), ('amount', '=', str(igst)),
                             ('type_tax_use', '=', "purchase"),
                             ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                    if tax_variant:
                        tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                    else:
                        tax = False

                    product_id = product and request.env['product.product'].sudo().search(
                        [('name', '=', product)], limit=1) or False

                    customer = row["master"]["partner_id"]["customer_name"]
                    code = row["master"]["partner_id"]["code"]

                    if code:
                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('code', 'like',code), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        # print(analytical_id.id)
                        if not analytical_id:
                            analytical_details = {
                                    'name': row["master"]["partner_id"]["customer_name"],
                                    'code': row["master"]["partner_id"]["code"],
                                    'company_id': to_company_detail2.id,
                                        }
                            analytical_id = request.env['account.analytic.account'].sudo().create(analytical_details)


                        analytical_id = request.env['account.analytic.account'].sudo().search(
                            [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False


                    invoice_line_ids.append((0, 0, {
                        'display_type': False,
                        'quantity': quantity,
                        'product_id': product_id,
                        'product_uom_id': product_id.uom_id.id,
                        'price_unit': price,
                        'tax_ids':tax_variant,
                        'analytic_account_id':analytical_id,
                         # 'account_id':coa_id,


                    }))
            if vendor:
                purchase_order_1 = request.env['account.move'].sudo().create({
                    'move_type':"out_refund",
                    'partner_id': vendor.id,
                    'company_id':to_company_detail2.id,
                    'journal_id':jounal_id.id,
                    # 'ref':reference,
                    'invoice_date':date,
                    'date':date,
                    'invoice_line_ids': invoice_line_ids,
                })
                request.env.cr.commit()

                if purchase_order_1:
                    credit_note_no.append({
                        'Credit_Note_Number': purchase_order_1.name,

                    })
        return credit_note_no

