import json
import qrcode
import base64
from io import BytesIO

from odoo import api, models, fields, _
import requests

from datetime import datetime


class IrnInherit(models.Model):
    _inherit = "account.move"

    tax_sh = fields.Char(string="Tax sch")
    sup_typ = fields.Char(string="Sup Typ")
    reg_rev = fields.Char(string="Reg Rev")
    ecm_gstin = fields.Char(string="ECM Gstin")
    igst_on_intra = fields.Char(string="IGST On Intra")
    name1 = fields.Char(string="Name")
    Addr_1 = fields.Char(string="Address")
    Addr_2 = fields.Char(string="Address 2")
    loc = fields.Char(string="Location")
    pin = fields.Char(string="Pin")
    stcd = fields.Char(string="State Code")
    Gstin = fields.Char(string="Gstin *")
    LglNm = fields.Char(string="Legal Name *")
    TrdNm = fields.Char(string="Trade Name")
    Addrs1 = fields.Char(string="Address * ")
    Addrs2 = fields.Char(string="Address 2")
    Loc1 = fields.Char(string="Location *")
    Pin1 = fields.Char(string="Pin*")
    stcd1 = fields.Char(string="State Code *")

    ShipBNo = fields.Char(string="Shipping Bill No *")
    ShipBDt = fields.Date(string="Shipping Bill Date *")
    Port = fields.Char(string="Port *")
    RefClm = fields.Char(string="RefClm")
    ForCur = fields.Char(string="Currency")
    CntCode = fields.Char(string="Country Code")
    # TransId = fields.Char(string="Transport Id")
    # TransName = fields.Char(string="Transport Name")
    Distance = fields.Char(string="Distance")
    # TransDocNo = fields.Char(string="Transport DocNo")
    # TransDocDt = fields.Date(string="Transport Doc Date *")
    # VehNo = fields.Char(string="Vehicle No")
    # VehType = fields.Char(string="Vehicle Type")
    # TransMode = fields.Char(string="Transport Mode")
    Success = fields.Char(string="Success")
    AckNo = fields.Char(string="Acknowledgment No")
    AckDt = fields.Date(string="Acknowledgment Date")
    Irn = fields.Char(string="IRN")
    SignedInvoice = fields.Char(string="Signed Invoice")
    Status = fields.Char(string="Status")
    # EwbNo = fields.Char(string="EWB No")
    # EwbDt = fields.Date(string="EWB Date")
    # EwbValidTill = fields.Date(string="EWB Valid Till")
    # log = fields.Char(string="Log")
    govt_log = fields.Char(string="Government Log")
    log = fields.Char(string="Log")
    qr_code = fields.Binary("Signed QRCode", attachment=True, store=True)


class SaleOrderInherit(models.Model):
    _inherit = 'account.move'

    def action_generate_irn(self):

        # if not self.TransDocDt:
        #     raise self.env['res.config.settings'].get_config_warning("Enter Transportation Date")

        sample_str = self.company_id.partner_id.vat
        state_code = sample_str[0:2]

        sampl_str = self.partner_id.vat
        state_code1 = sampl_str[0:2]

        #         Clear Tax Sandbox Credentials for Testing
        #         company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
        #         company_auth_token = "1.0e34e660-c559-4ad5-ab87-b53547ebd091_8f680e5750e447de7676af3ba12197022d98029bdae09955fe1b332a99e6e391"
        #         company_gstin = "32AAACE6765D1ZX"

        comp_gstin = self.warehouse_id.partner_id.vat

        #         Clear Tax Credentials for Production

        company_auth_token = "1.57ed9a8b-b597-41d5-89f2-81086db2c327_abdbe987b4f20506778017c6e1bc8d7c3b06547fc4de158b14eeb57f5a2bf2e4"
        if (comp_gstin == "32AAACE6765D1ZX"):
            company_owner_id = "49233995-7680-4fbb-ad7d-95766ea24505"
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

        #         url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/generate"
        url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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

        for items in self.invoice_line_ids:
            print(items.tax_ids.amount)
            GstRt = 0.0
            SgstAmt = 0.0
            CgstAmt = 0.0
            IgstAmt = 0.0

            if items.tax_ids.name.startswith('GST'):
                GstRt = items.tax_ids.amount
                GstAmt = (((items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                        items.discount / 100))) * items.tax_ids.amount) / 100
                IgstAmt = 0.0
                CgstAmt = (GstAmt / 2)
                SgstAmt = (GstAmt / 2)

            elif items.tax_ids.name.startswith('IGST'):
                GstRt = items.tax_ids.amount
                GstAmt = (((items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                        items.discount / 100))) * items.tax_ids.amount) / 100
                IgstAmt = GstAmt
                CgstAmt = 0.0
                SgstAmt = 0.0

            total = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                    items.discount / 100)) + GstAmt

            pdt_cat= items.product_id.detailed_type
            print(pdt_cat)
            if pdt_cat == "service":
                servc ="Y"
            else:
                servc="N"


            item_dict = {
                "SlNo": count,
                "PrdDesc": items.name,
                "IsServc": servc,
                "HsnCd": items.product_id.l10n_in_hsn_code,
                "Qty": items.quantity,
                #                 "Unit": items.product_id.uom_id.name,
                "Unit": "NOS",
                "UnitPrice": items.price_unit,
                "TotAmt": items.quantity * items.price_unit,
                "Discount": (items.quantity * items.price_unit) * (items.discount / 100),
                "AssAmt": (items.quantity * items.price_unit) - (
                        (items.quantity * items.price_unit) * (items.discount / 100)),
                "GstRt": GstRt,
                "IgstAmt": IgstAmt,
                "CgstAmt": CgstAmt,
                "SgstAmt": SgstAmt,
                "TotItemVal": total,
            }

            count = count + 1
            TotalAssVal = TotalAssVal + ((items.quantity * items.price_unit) - (
                    (items.quantity * items.price_unit) * (items.discount / 100)))
            TotalCgstVal = TotalCgstVal + CgstAmt
            TotalSgstVal = TotalSgstVal + CgstAmt
            TotalIgstVal = TotalIgstVal + IgstAmt
            TotInvVal = TotInvVal + total
            item_list.append(item_dict)

        testeddate = self.invoice_date
        Invoicedate = datetime.strftime(testeddate, '%d/%m/%Y')
        ShipBDt = False
        if self.ShipBDt:
            shdate = self.ShipBDt
            ShipBDt = datetime.strftime(shdate, '%d/%m/%Y')
        trandt = self.TransDocDt
        TransDocDt = datetime.strftime(trandt, '%d/%m/%Y')
        formated_original = [
            {
                "transaction": {
                    "Version": "1.1",
                    "TranDtls": {
                        "TaxSch": "GST",
                        "SupTyp": "B2B",
                        "EcmGstin": None,
                        "IgstOnIntra": "N"
                    },
                    "DocDtls": {
                        "Typ": "INV",
                        "No": self.name,
                        "Dt": Invoicedate
                    },
                    "SellerDtls": {
                        "Gstin": self.warehouse_id.partner_id.vat,
                        "LglNm": self.warehouse_id.partner_id.name,
                        "TrdNm": self.warehouse_id.partner_id.name,
                        "Addr1": self.warehouse_id.partner_id.street,
                        "Loc": self.warehouse_id.partner_id.street2,
                        "Pin": self.warehouse_id.partner_id.zip,
                        "Stcd": state_code,
                    },
                    "BuyerDtls": {
                        "Gstin": self.partner_id.vat,
                        "LglNm": self.partner_id.name,
                        "TrdNm": self.partner_id.name,
                        "Pos": state_code1,
                        "Addr1": self.partner_id.street,
                        "Loc": self.partner_id.street2,
                        "Pin": self.partner_id.zip,
                        "Stcd": state_code1,
                    },
                    "ShipDtls": {
                        "Gstin": self.partner_id.vat,
                        "LglNm": self.partner_id.name,
                        "TrdNm": self.partner_id.name,
                        "Addr1": self.partner_id.street,
                        "Loc": self.partner_id.street2,
                        "Pin": self.partner_id.zip,
                        "Stcd": state_code1,
                    },
                    #                     "ShipDtls": {
                    #                         "Gstin": self.Gstin,
                    #                         "LglNm": self.LglNm,
                    #                         "TrdNm": self.TrdNm,
                    #                         "Addr1": self.Addrs1,
                    #                         "Addr2": self.Addrs2,
                    #                         "Loc": self.Loc1,
                    #                         "Pin": self.Pin1,
                    #                         "Stcd": self.stcd1
                    #                     },
                    "ItemList": item_list,

                    "ValDtls": {
                        "AssVal": TotalAssVal,
                        "CgstVal": TotalCgstVal,
                        "SgstVal": TotalSgstVal,
                        "IgstVal": TotalIgstVal,
                        "Discount": 0,
                        "TotInvVal": TotInvVal
                    },

                    #                     "ExpDtls": {
                    #                         "ShipBNo": self.ShipBNo,
                    #                         "ShipBDt": ShipBDt
                    #                     },
                    # "EwbDtls": {
                    #     #                         "TransId": self.TransId,
                    #     #                         "TransName": self.TransName,
                    #     #                         "Distance": self.Distance,
                    #     #                         "TransDocNo": self.TransDocNo,
                    #     "TransDocDt": TransDocDt,
                    #     "VehNo": self.vehicle_no,
                    #     "VehType": "R",
                    #     "TransMode": 1
                    # }
                }

            }
        ]
        try:
            req = requests.put(url, data=json.dumps(formated_original), headers=headers, timeout=50)
            req.raise_for_status()
            content = req.json()

            if content[0]['govt_response']['Success'] == 'Y':
                self.Irn = content[0]['govt_response']['Irn'] if content[0]['govt_response'][
                                                                     'Success'] == 'Y' else False
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                print("generate QR CODE")
                qr.add_data(self.Irn)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                self.qr_code = qr_image

                self.govt_log = content[0]['govt_response']['Status']
                self.AckNo = content[0]['govt_response']['AckNo']
                self.AckDt = content[0]['govt_response']['AckDt']
                # self.EwbNo = content[0]['govt_response']['EwbNo']
                # self.EwbDt = content[0]['govt_response']['EwbDt']
                # self.EwbValidTill = content[0]['govt_response']['EwbValidTill']
                self.Success = content[0]['govt_response']['Success']
                self.SignedInvoice = content[0]['govt_response']['SignedInvoice']

            else:
                self.Irn = False
                self.govt_log = content[0]['govt_response']['ErrorDetails']
            self.log = content[0]['document_status']

        except IOError:
            error_msg = _("Required Fields Missing or Invalid Format For IRN generation.")
            raise self.env['res.config.settings'].get_config_warning(error_msg)