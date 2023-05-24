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
    TransId = fields.Char(string="Transport Id")
    TransName = fields.Char(string="Transport Name")
    Distance = fields.Char(string="Distance *")
    TransDocNo = fields.Char(string="Transport DocNo")
    TransDocDt = fields.Date(string="Transport Doc Date *")
    VehNo = fields.Char(string="Vehicle No *")
    VehType = fields.Char(string="Vehicle Type *")
    TransMode = fields.Char(string="Transport Mode *")
    Success = fields.Char(string="Success")
    AckNo = fields.Char(string="Acknowledgment No")
    AckDt = fields.Date(string="Acknowledgment Date")
    Irn = fields.Char(string="IRN")
    SignedInvoice = fields.Char(string="Signed Invoice")
    Status = fields.Char(string="Status")
    EwbNo = fields.Char(string="EWB No")
    EwbDt = fields.Date(string="EWB Date")
    EwbValidTill = fields.Date(string="EWB Valid Till")
    log = fields.Char(string="Log")
    govt_log = fields.Char(string="Government Log")
    qr_code = fields.Binary("Signed QRCode", attachment=True, store=True)


class SaleOrderInherit(models.Model):
    _inherit = 'account.move'

    def action_generate_irn(self):

        if not self.TransDocDt:
            raise self.env['res.config.settings'].get_config_warning("Enter Transportation Date")
        
        if self.ShipBDt:

            sample_str = self.company_id.vat
            state_code = sample_str[0:2]

            sample_str = "32AAACE6765D1ZX"
            state_code = sample_str[0:2]

            sampl_str = self.partner_id.vat
            if sampl_str == "URP":                
                state_code1 = 96
                
            else:
                state_code1 = sampl_str[0:2]

            # ship_state_code = self.deliver_to.vat
            # ship_state_code1 = False
            # if ship_state_code:
            #     ship_state_code1 = ship_state_code[0:2]

            #         Clear Tax Sandbox Credentials for Testing
            #         company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
            #         company_auth_token = "1.0e34e660-c559-4ad5-ab87-b53547ebd091_8f680e5750e447de7676af3ba12197022d98029bdae09955fe1b332a99e6e391"
            #         company_gstin = "32AAACE6765D1ZX"

            comp_gstin = self.company_id.vat
            # comp_gstin = "33AACCE3723D1Z9"

            #         Clear Tax Credentials for Production 
            company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
            if (comp_gstin == "32AAACE6765D1ZX"):
                company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                company_gstin = "32AAACE6765D1ZX"

            #         company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
            #         if (comp_gstin == "32AACCE3723D1ZB"):
            #             company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
            #             company_gstin = "32AACCE3723D1ZB"

            elif (comp_gstin == "33AACCE3723D1Z9"):
                company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                company_gstin = "33AACCE3723D1Z9"

            else:
                error_msg = _("Please Check the GST Details")
                raise self.env['res.config.settings'].get_config_warning(error_msg)

            url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/generate"
            # url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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

                inr_cost = items.cost_in_inr_cur / items.quantity
                price = float(inr_cost)

                print(items.tax_ids.amount)
                GstRt = 0.0
                SgstAmt = 0.0
                CgstAmt = 0.0
                IgstAmt = 0.0

                if items.tax_ids.name.startswith('GST'):
                    GstRt = items.tax_ids.amount
                    GstAmt = (((items.quantity * price) - ((items.quantity * price) * (
                            items.discount / 100))) * items.tax_ids.amount) / 100
                    IgstAmt = 0.0
                    CgstAmt = (GstAmt / 2)
                    SgstAmt = (GstAmt / 2)

                elif items.tax_ids.name.startswith('IGST'):
                    GstRt = items.tax_ids.amount
                    GstAmt = (((items.quantity * price) - ((items.quantity * price) * (
                            items.discount / 100))) * items.tax_ids.amount) / 100
                    IgstAmt = GstAmt
                    CgstAmt = 0.0
                    SgstAmt = 0.0

                total = (items.quantity * price) - ((items.quantity * price) * (
                        items.discount / 100)) + GstAmt

                # inr_cost = items.cost_in_inr_cur / items.quantity
                # price = float(inr_cost)



                IsServc = "N"
                if items.product_id.detailed_type == "service":
                    IsServc = "Y"
                item_dict = {
                    "SlNo": count,
                    "PrdDesc": items.name,
                    #                 "IsServc": "Y",
                    "IsServc": IsServc,
                    "HsnCd": items.product_id.l10n_in_hsn_code,
                    "Qty": items.quantity,
                    #                 "Unit": items.product_id.uom_id.name,
                    "Unit": "KG",
                    "UnitPrice": price,
                    "TotAmt": items.quantity * price,
                    "Discount": (items.quantity * price) * (items.discount / 100),
                    "AssAmt": (items.quantity * price) - (
                            (items.quantity * price) * (items.discount / 100)),
                    "GstRt": GstRt,
                    "IgstAmt": IgstAmt,
                    "CgstAmt": CgstAmt,
                    "SgstAmt": SgstAmt,
                    "TotItemVal": total,
                }

                count = count + 1
                TotalAssVal = TotalAssVal + ((items.quantity * price) - (
                        (items.quantity * price) * (items.discount / 100)))
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

            if self.move_type == "out_invoice":
                doctype = "INV"
            if self.move_type == "out_refund":
                doctype = "CRN"
            if self.move_type == "in_refund":
                doctype = "DBN"

            formated_original = [
                {
                    "transaction": {
                        "Version": "1.1",
                        "TranDtls": {
                            "TaxSch": "GST",
                            "SupTyp": "EXPWP",
                            "EcmGstin": None,
                            "IgstOnIntra": "N"
                        },
                        "DocDtls": {
                            "Typ": doctype,
                            "No": self.name,
                            "Dt": Invoicedate
                        },
                        "SellerDtls": {
                            "Gstin": self.company_id.vat,
                            "LglNm": self.company_id.name,
                            "TrdNm": self.company_id.name,
                            "Addr1": self.company_id.street,
                            "Loc": self.company_id.street2,
                            "Pin": self.company_id.zip,
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
    #                     "ShipDtls": {
    #                         "Gstin": self.partner_id.vat,
    #                         "LglNm": self.partner_id.name,
    #                         "TrdNm": self.partner_id.name,
    #                         "Addr1": self.partner_id.street,
    #                         "Loc": self.partner_id.street2,
    #                         "Pin": self.partner_id.zip,
    #                         "Stcd": state_code1,
    #                     },
    #                     "ShipDtls": {
    #                         "Gstin": self.partner_id.vat or False,
    #                         "LglNm": self.partner_id.name or False,
    #                         "TrdNm": self.partner_id.name or False,
    #                         "Addr1": self.partner_id.street or False,
    #                         "Loc": self.partner_id.street2 or False,
    #                         "Pin": self.partner_id.zip or False,
    #                         "Stcd": state_code1,
    # #                         "Stcd": 33,
    #                     },
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

                            "ExpDtls": {
                                "ShipBNo": self.ShipBNo,
                                "ShipBDt": ShipBDt
                            },
    #                      "EwbDtls": {
    #  #                         "TransId": self.TransId,
    #  #                         "TransName": self.TransName,
    #  #                         "Distance": self.Distance,
    #  #                         "TransDocNo": self.TransDocNo,
    #                          "TransDocDt": TransDocDt,
    #                          "VehNo": self.VehNo,
    #                          "VehType": "R",
    #                          "TransMode": 1
    #                      }
                    }

                }
            ]
        else:
            sample_str = self.company_id.vat
            state_code = sample_str[0:2]

            sampl_str = self.partner_id.vat
            if sampl_str:
                state_code1 = sampl_str[0:2]
            else:
                state_code1 = 99
                
            # ship_state_code = self.deliver_to.vat
            # ship_state_code1 = False
            # if ship_state_code:
            #     ship_state_code1 = ship_state_code[0:2]

            #         Clear Tax Sandbox Credentials for Testing
            #         company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
            #         company_auth_token = "1.0e34e660-c559-4ad5-ab87-b53547ebd091_8f680e5750e447de7676af3ba12197022d98029bdae09955fe1b332a99e6e391"
            #         company_gstin = "32AAACE6765D1ZX"

            comp_gstin = self.company_id.vat

            #         Clear Tax Credentials for Production 
            company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
            if (comp_gstin == "32AAACE6765D1ZX"):
                company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                company_gstin = "32AAACE6765D1ZX"

            #         company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
            #         if (comp_gstin == "32AACCE3723D1ZB"):
            #             company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
            #             company_gstin = "32AACCE3723D1ZB"

            elif (comp_gstin == "33AACCE3723D1Z9"):
                company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                company_gstin = "33AACCE3723D1Z9"

            else:
                error_msg = _("Please Check the GST Details")
                raise self.env['res.config.settings'].get_config_warning(error_msg)

            url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/generate"
            # url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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
                IsServc = "N"
                if items.product_id.detailed_type == "service":
                    IsServc = "Y"
                item_dict = {
                    "SlNo": count,
                    "PrdDesc": items.name,
                    #                 "IsServc": "Y",
                    "IsServc": IsServc,
                    "HsnCd": items.product_id.l10n_in_hsn_code,
                    "Qty": items.quantity,
                    #                 "Unit": items.product_id.uom_id.name,
                    "Unit": "KG",
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

            if self.move_type == "out_invoice":
                doctype = "INV"
            if self.move_type == "out_refund":
                doctype = "CRN"
            if self.move_type == "in_refund":
                doctype = "DBN"

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
                                "Typ": doctype,
                                "No": self.name,
                                "Dt": Invoicedate
                            },
                            "SellerDtls": {
                                "Gstin": self.company_id.vat,
                                "LglNm": self.company_id.name,
                                "TrdNm": self.company_id.name,
                                "Addr1": self.company_id.street,
                                "Loc": self.company_id.street2,
                                "Pin": self.company_id.zip,
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
                            # "ShipDtls": {
                            #     "Gstin": self.partner_id.vat or False,
                            #     "LglNm": self.partner_id.name or False,
                            #     "TrdNm": self.partner_id.name or False,
                            #     "Addr1": self.partner_id.street or False,
                            #     "Loc": self.partner_id.street2 or False,
                            #     "Pin": self.partner_id.zip or False,
                            #     "Stcd": state_code1,
                            # },
                            "ItemList": item_list,

                            "ValDtls": {
                                "AssVal": TotalAssVal,
                                "CgstVal": TotalCgstVal,
                                "SgstVal": TotalSgstVal,
                                "IgstVal": TotalIgstVal,
                                "Discount": 0,
                                "TotInvVal": TotInvVal
                            },
                        }
                    }
                ]
            
        try:
            req = requests.put(url, data=json.dumps(formated_original), headers=headers, timeout=50)
            req.raise_for_status()
            content = req.json()
            print(content)

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

                self.govt_log = content[0]['govt_response']['Status'] or "Not Applicable"
                self.AckNo = content[0]['govt_response']['AckNo'] or "Not Applicable"
                self.AckDt = content[0]['govt_response']['AckDt'] or "Not Applicable"
                # self.EwbNo = content[0]['govt_response']['EwbNo'] or "Not Applicable"
                # self.EwbDt = content[0]['govt_response']['EwbDt'] or "Not Applicable"
                # self.EwbValidTill = content[0]['govt_response']['EwbValidTill'] or "Not Applicable"
                self.Success = content[0]['govt_response']['Success'] or "Not Applicable"
                self.SignedInvoice = content[0]['govt_response']['SignedInvoice'] or "Not Applicable"

            else:
                self.Irn = False
                self.govt_log = content[0]['govt_response']['ErrorDetails'] or "Not Applicable"
            self.log = content[0]['document_status'] or "Not Applicable"

        except IOError:
            error_msg = _("Required Fields Missing or Invalid Format For IRN generation.")
            raise self.env['res.config.settings'].get_config_warning(error_msg)
