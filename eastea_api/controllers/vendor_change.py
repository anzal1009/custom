from odoo import http
from odoo.exceptions import ValidationError, UserError
from odoo.http import request, _logger
from datetime import datetime
from odoo import api, models, fields, _


class VendorChanger(http.Controller):

    @http.route('/vendor/change', type='json', csrf=False, auth='public')
    def vendor_changer(self, **rec):

        if request.jsonrequest:
            journal_number = []
            for row in rec["data"]:
                po_no = row['po_no']
                vendor_gst = row['vendor_gst']

                purchase_order_1 = po_no and request.env['purchase.order'].sudo().search([('name', '=', po_no)],
                                                                                         limit=1) or False
                vendor_id = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
                                                                                    limit=1) or False

                if purchase_order_1:
                    purchase_order_1.partner_id = vendor_id.id
                    purchase_order_1.action_view_picking()
                    if purchase_order_1.picking_ids:
                        purchase_order_1.picking_ids.partner_id = vendor_id.id
                        # purchase_order_1.action_create_invoice()

                    purchase_inv = request.env['account.move'].sudo().search(
                        [('invoice_origin', '=', purchase_order_1.name)], limit=1)
                    date = purchase_inv.date
                    analytical = purchase_inv.invoice_line_ids.analytic_account_id
                    account = purchase_inv.invoice_line_ids.account_id
                    billref = purchase_inv.ref
                    payref = purchase_inv.payment_reference
                    journal = purchase_inv.journal_id
                    due = purchase_inv.invoice_date_due
                    # print(account.id)
                    # print(analytical.id)
                    if purchase_inv:
                        purchase_inv.button_draft()
                        purchase_inv.name = ""
                        request.env.cr.commit()
                        unlink = purchase_inv.unlink()
                        request.env.cr.commit()
                        if unlink:
                            purchase_order_1.action_create_invoice()
                            invoice = request.env['account.move'].sudo().search([('invoice_origin', '=', purchase_order_1.name)], limit=1)
                            if invoice:
                                invoice.date = date
                                invoice.ref = billref
                                invoice.payment_reference = payref
                                invoice.journal_id = journal.id
                                invoice.invoice_date_due = date
                                invoice.invoice_line_ids.analytic_account_id = analytical.id
                                invoice.invoice_line_ids.account_id = account.id

                                invoice2 = request.env['account.move'].sudo().search([('invoice_origin', '=', purchase_order_1.name)], limit=1)
                                if invoice2:
                                    # invoice2.l10n_in_gst_treatment = purchase_inv.l10n_in_gst_treatment.id
                                    invoice2.invoice_date = date
                                    invoice2.action_post()
                                    invoice.date = date
                                    invoice.ref = billref
                                    invoice.invoice_date_due = date
                                    request.env.cr.commit()
                                    # invoice.date = date













    # @http.route('/vendor/change', type='json', csrf=False, auth='public')
    # def vendor_changer(self, **rec):
    #
    #     if request.jsonrequest:
    #         journal_number = []
    #         for row in rec["data"]:
    #             po_no = row['po_no']
    #             vendor_gst = row['vendor_gst']
    #
    #             po_id = po_no and request.env['purchase.order'].sudo().search([('name', '=', po_no)],
    #             limit=1) or False
    #             # print(po_id.partner_id.name)
    #             vendor_id = vendor_gst and request.env['res.partner'].sudo().search([('vat', '=', vendor_gst)],
    #             limit=1) or False
    #             # print(vendor_id.name)
    #
    #             if vendor_id:
    #                 po_id.partner_id.name = vendor_id.name
