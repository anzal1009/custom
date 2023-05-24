import json
from io import BytesIO
from odoo import api, models, fields, _
import requests
from datetime import datetime


class InventoryTransfersIrn(models.Model):
    _inherit = 'stock.move'

    price = fields.Float("Price", related='product_id.standard_price', tracking=True, readonly=False)
    taxes_id = fields.Many2one("account.tax", "Taxes")
    sub_totals = fields.Float("Subtotal")


#     @api.depends('qty_done','price')
#     def compute_sub_totals(self):
#         for row in self:
#             row.sub_totals = row.qty_done * row.price
#             return row.total
# print(total)


class IrnButton(models.Model):
    _inherit = 'stock.picking'

    TransMode = fields.Char("Transport Mode")
    TransDocDt = fields.Date("Transport Date")
    VehNo = fields.Char("Vehicle No")
    VehType = fields.Char("Vehicle Type")
    Distance = fields.Char("Distance")
    EwbNo = fields.Char("Eway No")
    EwbDt = fields.Char("Eway Date")
    EwbValidTill = fields.Char("E-Valide Date")
    ewb_status = fields.Char("E-Status")
    elog = fields.Char("E-Log")
    Status = fields.Char("Status")
    transid = fields.Char("Transaction Id")
    transgst = fields.Char("Transporter GST")

    def action_irnt(self):
        print("yy")
        if not self.TransDocDt:
            raise self.env['res.config.settings'].get_config_warning("Enter Transportation Date")


        # company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
        # company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
        # company_gstin = "32AAACE6765D1ZX"

        comp_gstin = self.warehouse_id.partner_id.vat

        #         Clear Tax Credentials for Production

        company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
        if (comp_gstin == "32AAACE6765D1ZX"):
            company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
            company_gstin = "32AAACE6765D1ZX"

        elif (comp_gstin == "33AAACE6765D1ZV"):
            company_owner_id = "b2c91294-cd23-4218-9352-35d119e556c4"
            company_gstin = "33AAACE6765D1ZV"

        elif (comp_gstin == "29AAACE6765D1ZK"):
            company_owner_id = "e7b097d9-4091-45b3-9e45-d4909b977ed3"
            company_gstin = "29AAACE6765D1ZK"

        elif (comp_gstin == "27AAACE6765D2ZN"):
            company_owner_id = "1323721e-7aab-4461-84af-b698f433ad99"
            company_gstin = "27AAACE6765D2ZN"

        else:
            error_msg = _("Please Check the GST Details")
            raise self.env['res.config.settings'].get_config_warning(error_msg)

        sample_str = self.location_id.partner_id.vat
        disstc = sample_str[0:2]

        sampl_str = self.location_dest_id.partner_id.vat
        Stcd = sampl_str[0:2]

        testeddate = self.TransDocDt
        transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

        if self.transgst:
            trsportgst = self.transgst
        else:
            trsportgst = self.location_dest_id.partner_id.vat

        # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
        # url = "https://einvoicing.internal.cleartax.co/v3/ewaybill/generate"
        # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
        url = "https://api-einv.cleartax.in/einv/v3/ewaybill/generate"
        # url = "http://99.83.130.139/einv/v3/ewaybill/generate"
        headers = {"Content-type": "application/json",
                   "x-cleartax-auth-token": company_auth_token,
                   "x-cleartax-product": "EInvoice", "owner_id": company_owner_id,
                   "gstin": company_gstin}
        item_list = []
        count = 1
        TotalAssVal = 0
        TotalCgstVal = 0
        TotalSgstVal = 0
        TotalIgstVal = 0
        TotInvVal = 0

        for items in self.move_ids_without_package:
            print(items.taxes_id.amount)
            GstRt = 0.0
            iGstRt = 0.0
            SgstAmt = 0.0
            CgstAmt = 0.0
            IgstAmt = 0.0

            #             if items.taxes_id.name.startswith('GST'):
            #                 GstRt = items.taxes_id.amount
            GstAmt = 0.0
            #                 IgstAmt = 0.0
            #                 CgstAmt = (GstAmt / 2)
            #                 SgstAmt = (GstAmt / 2)

            #             elif items.taxes_id.name.startswith('IGST'):
            #                 iGstRt = items.taxes_id.amount
            GstAmt = 0.0
            #                 IgstAmt = GstAmt
            #                 CgstAmt = 0.0
            #                 SgstAmt = 0.0

            total = ((items.quantity_done * items.price)) + GstAmt
            print(total)

            item_dict = {
                "SlNo": count,
                "ProdName": items.name,
                "PrdDesc": items.name,
                #                 "IsServc": "Y",
                # "IsServc": "N",
                "HsnCd": items.product_id.l10n_in_hsn_code,
                "Qty": items.quantity_done,
                #                 "Unit": items.product_id.uom_id.name,
                "Unit": "NOS",
                # "UnitPrice": items.price_unit,
                # "TotAmt": items.quantity * items.price_unit,
                # "Discount": (items.quantity * items.price_unit) * (items.discount / 100),
                "AssAmt": (items.quantity_done * items.price),
                # "GstRt": GstRt,
                "CgstRt": 0,
                "SgstRt": 0,
                "IgstRt": 0,
                "IgstAmt": 0,
                "CgstAmt": 0,
                "SgstAmt": 0,
                "TotItemVal": total,
            }
            count = count + 1
            TotalAssVal = TotalAssVal + ((items.quantity_done * items.price))
            TotalCgstVal = 0
            TotalSgstVal = 0
            TotalIgstVal = 0
            TotInvVal = TotInvVal + total
            print(TotalAssVal)
            print(TotalCgstVal)
            print(TotalSgstVal)
            print(TotalIgstVal)
            print(TotInvVal)
            item_list.append(item_dict)
        #
        # sampl_str = self.name
        # doc = sampl_str[0:3]

        # if self.move_type == "out_invoice":
        #     doc = "INV"
        # if self.move_type == "out_refund":
        #     doc = "OTH"
        # if self.move_type == "in_refund":
        #     doc = "OTH"
        # if doc == "INV":
        #     sub = "SUPPLY"
        # if doc == "OTH":
        #     sub = "OTH"
        doc = "CHL"
        sub = "OWN_USE"

        inv_date = self.date_done
        doc_date = datetime.strftime(testeddate, '%d/%m/%Y')

        datas3 = {
            "DocumentNumber": self.name,
            "DocumentType": doc,
            "DocumentDate": doc_date,
            "SupplyType": "OUTWARD",
            "SubSupplyType": sub,
            "SubSupplyTypeDesc": "Others",
            "TransactionType": "Regular",
            "BuyerDtls": {
                "Gstin": self.location_dest_id.partner_id.vat,
                "LglNm": self.location_dest_id.partner_id.name,
                "TrdNm": self.location_dest_id.partner_id.name,
                "Addr1": self.location_dest_id.partner_id.street,
                "Addr2": self.location_dest_id.partner_id.street2,
                "Loc": self.location_dest_id.partner_id.city,
                "Pin": self.location_dest_id.partner_id.zip,
                "Stcd": Stcd,
            },
            "SellerDtls": {
                "Gstin": self.location_id.partner_id.vat,
                "LglNm": self.location_id.partner_id.name,
                "TrdNm": self.location_id.partner_id.name,
                "Addr1": self.location_id.partner_id.street,
                "Addr2": self.location_id.partner_id.street2,
                "Loc": self.location_id.partner_id.city,
                "Pin": self.location_id.partner_id.zip,
                "Stcd": disstc,
            },
            "ItemList": item_list,
            "TotalInvoiceAmount": TotInvVal,
            "TotalCgstAmount": TotalCgstVal,
            "TotalSgstAmount": TotalSgstVal,
            "TotalIgstAmount": TotalIgstVal,
            "TotalCessAmount": None,
            "TotalCessNonAdvolAmount": None,
            "TotalAssessableAmount": TotalAssVal,
            "OtherAmount": None,
            "OtherTcsAmount": None,
            "TransId": trsportgst,
            "TransName": "TRANSPORT",
            "TransMode": self.TransMode,
            "Distance": self.Distance,
            "VehNo": self.VehNo,
            "VehType": None
        }

        print(datas3)

        try:
            req = requests.put(url, data=json.dumps(datas3), headers=headers, timeout=50)
            req.raise_for_status()
            content = req.json()
            print(content)

            if content['govt_response']['Success'] == 'Y':
                self.elog = content['govt_response']['EwbNo'] if content['govt_response'][
                                                                     'Success'] == 'Y' else False
                self.Status = content['govt_response']['Success']
                self.ewb_status = content['ewb_status']
                #     # self.AckNo = content[0]['govt_response']['AckNo']
                #     # self.AckDt = content[0]['govt_response']['AckDt']
                self.EwbNo = content['govt_response']['EwbNo']
                self.EwbDt = content['govt_response']['EwbDt']
                self.EwbValidTill = content['govt_response']['EwbValidTill']
                self.Status = content['govt_response']['Success']
                self.transid = content['transaction_id']
            #     # self.SignedInvoice = content[0]['govt_response']['SignedInvoice']
            #
            else:
                self.EwbNo = False
                self.elog = content['govt_response']['ErrorDetails']
                self.ewb_status = content['ewb_status'] or "Not Applicable"

        except IOError:
            error_msg = _("Required Fields Missing or Invalid Format For EWAY generation.")
            raise self.env['res.config.settings'].get_config_warning(error_msg)