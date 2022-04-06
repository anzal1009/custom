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
    # name2 = fields.Char(string="Name")
    # Val = fields.Char(string="Val")
    #
    # AssVal = fields.Char(string="AssVal")
    # CgstVal = fields.Char(string="CgstVal")
    # SgstVal = fields.Char(string="SgstVal")
    # IgstVal = fields.Char(string="IgstVal")
    # CesVal = fields.Char(string="CesVal")
    # StCesVal = fields.Char(string="StCesVal")
    # Discount = fields.Char(string="Discount")
    # OthChrg = fields.Char(string="OthChrg")
    # RndOffAmt = fields.Char(string="RndOffAmt")
    # TotInvVal = fields.Char(string="TotInvVal")
    # TotInvValFc = fields.Char(string="TotInvValFc")
    #
    # name3 = fields.Char(string="Name")
    # AccDet = fields.Char(string="AccDet")
    # Mode = fields.Char(string="Mode")
    # FinInsBr = fields.Char(string="FinInsBr")
    # PayTerm = fields.Char(string="PayTerm")
    # PayInstr = fields.Char(string="PayInstr")
    # CrTrn = fields.Char(string="CrTrn")
    # DirDr = fields.Char(string="DirDr")
    # CrDay = fields.Char(string="CrDay")
    # PaidAmt = fields.Char(string="PaidAmt")
    # PaymtDue = fields.Char(string="PaymtDue")
    ShipBNo = fields.Char(string="Shipping Bill No *")
    ShipBDt = fields.Date(string="Shipping Bill Date *")
    Port = fields.Char(string="Port *")
    RefClm = fields.Char(string="RefClm")
    ForCur = fields.Char(string="Currency")
    CntCode = fields.Char(string="Country Code")
    TransId = fields.Char(string="Transaction Id")
    TransName = fields.Char(string="Transaction Name")
    Distance = fields.Char(string="Distance")
    TransDocNo = fields.Char(string="Transaction DocNo")
    TransDocDt = fields.Date(string="Transaction Doc Date *")
    VehNo = fields.Char(string="Vehicle No")
    VehType = fields.Char(string="Vehicle Type")
    TransMode = fields.Char(string="Transport Mode")
    Success = fields.Char(string="Success")
    AckNo = fields.Char(string="Acknowledgment No")
    AckDt = fields.Date(string="Acknowledgment Date")
    Irn = fields.Char(string="IRN")
    SignedInvoice = fields.Char(string="Signed Invoice")
    # qr_code = fields.Binary( string="Signed QRCode",attachment=True,store=True)
    Status = fields.Char(string="Status")
    EwbNo = fields.Char(string="EWB No")
    EwbDt = fields.Date(string="EWB Date")
    EwbValidTill = fields.Date(string="EWB Valid Till")
    log = fields.Char(string="Log")
    govt_log = fields.Char(string="Government Log")
    qr_code = fields.Binary("Signed QRCode", attachment=True, store=True)


#
class SaleOrderInherit(models.Model):
    _inherit = 'account.move'

    def action_generate_irn(self):
        sample_str = self.company_id.partner_id.vat
        state_code = sample_str[0:2]
        print(self.company_id.partner_id.vat)

        sampl_str = self.partner_id.vat
        state_code1 = sample_str[0:2]
        print(state_code1)

        print(self, "generate_irn")
        # Clear Tax Credentials
        company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
        company_auth_token = "1.0e34e660-c559-4ad5-ab87-b53547ebd091_8f680e5750e447de7676af3ba12197022d98029bdae09955fe1b332a99e6e391"
        company_gstin = "32AAACE6765D1ZX"

        url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/generate"
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
                print('gst')
                GstRt = items.tax_ids.amount
                GstAmt = (items.quantity * items.price_unit * items.tax_ids.amount) / 100
                IgstAmt = 0.0
                CgstAmt = GstAmt / 2
                SgstAmt = GstAmt / 2

            elif items.tax_ids.name.startswith('IGST'):
                print('igst')
                GstRt = items.tax_ids.amount
                GstAmt = (items.quantity * items.price_unit * items.tax_ids.amount) / 100
                IgstAmt = GstAmt
                CgstAmt = 0.0
                SgstAmt = 0.0

            total = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                    items.discount / 100)) + GstAmt

            item_dict = {
                "SlNo": count,
                "PrdDesc": items.name,
                "IsServc": "N",
                "HsnCd": items.product_id.l10n_in_hsn_code,
                "Qty": items.quantity,
                "Unit": items.product_id.uom_id.name,
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
            TotalAssVal = TotalAssVal + (items.quantity * items.price_unit)
            TotalCgstVal = TotalCgstVal + CgstAmt
            TotalSgstVal = TotalSgstVal + CgstAmt
            TotalIgstVal = TotalIgstVal + IgstAmt
            TotInvVal = TotInvVal + total
            item_list.append(item_dict)

        testeddate = self.invoice_date
        Invoicedate = datetime.strftime(testeddate, '%d/%m/%Y')
        shdate = self.ShipBDt
        ShipBDt = datetime.strftime(shdate, '%d/%m/%Y')
        trandt = self.TransDocDt
        TransDocDt = datetime.strftime(trandt, '%d/%m/%Y')
        print(TransDocDt)
        print(ShipBDt)
        print(item_list)

        formated_original = [
            {
                "transaction": {
                    "Version": "1.1",
                    "TranDtls": {
                        "TaxSch": self.tax_sh,
                        "SupTyp": self.sup_typ,
                        "EcmGstin": None,
                        "IgstOnIntra": "N"
                    },
                    "DocDtls": {
                        "Typ": "INV",
                        "No": self.name,
                        "Dt": Invoicedate
                    },
                    "SellerDtls": {
                        "Gstin": "32AAACE6765D1ZX",
                        "LglNm": self.company_id.partner_id.street,
                        "TrdNm": self.company_id.partner_id.street,
                        "Addr1": self.company_id.partner_id.street2,
                        "Loc": self.company_id.partner_id.city,
                        "Pin": self.company_id.partner_id.zip,
                        "Stcd": state_code,
                    },
                    "BuyerDtls": {
                        "Gstin": self.partner_id.vat,
                        "LglNm": self.partner_id.name,
                        "TrdNm": self.partner_id.name,
                        "Pos": state_code1,
                        "Addr1": self.partner_id.street,
                        "Loc": self.partner_id.state_id.name,
                        "Pin": self.partner_id.zip,
                        "Stcd": state_code1,
                    },
                    "ShipDtls": {
                        "Gstin": self.Gstin,
                        "LglNm": self.LglNm,
                        "TrdNm": self.TrdNm,
                        "Addr1": self.Addrs1,
                        "Addr2": self.Addrs2,
                        "Loc": self.Loc1,
                        "Pin": self.Pin1,
                        "Stcd": self.stcd1
                    },
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
                    "EwbDtls": {
                        "TransId": self.TransId,
                        "TransName": self.TransName,
                        "Distance": self.Distance,
                        "TransDocNo": self.TransDocNo,
                        "TransDocDt": TransDocDt,
                        "VehNo": self.VehNo,
                        "VehType": self.VehType,
                        "TransMode": self.TransMode
                    }
                }

            }
        ]
        print(formated_original)
        test_data = [
            {
                "transaction": {
                    "Version": "1.1",
                    "TranDtls": {
                        "TaxSch": "GST",
                        "SupTyp": "B2B",
                        "RegRev": "Y",
                        # "EcmGstin": null,
                        "IgstOnIntra": "N"
                    },
                    "DocDtls": {
                        "Typ": "INV",
                        "No": "DAOC/017",
                        "Dt": "04/04/2022"
                    },
                    "SellerDtls": {
                        "Gstin": "29AAFCD5862R000",
                        "LglNm": "NIC company pvt ltd",
                        "TrdNm": "NIC Industries",
                        "Addr1": "5th block, kuvempu layout",
                        "Addr2": "kuvempu layout",
                        "Loc": "GANDHINAGAR",
                        "Pin": 560037,
                        "Stcd": "29",
                        "Ph": "9000000000",
                        "Em": "abc@gmail.com"
                    },
                    "BuyerDtls": {
                        "Gstin": "29AWGPV7107B1Z1",
                        "LglNm": "XYZ company pvt ltd",
                        "TrdNm": "XYZ Industries",
                        "Pos": "12",
                        "Addr1": "7th block, kuvempu layout",
                        "Addr2": "kuvempu layout",
                        "Loc": "GANDHINAGAR",
                        "Pin": 562160,
                        "Stcd": "29",
                        "Ph": "91111111111",
                        "Em": "xyz@yahoo.com"
                    },
                    "DispDtls": {
                        "Nm": "ABC company pvt ltd",
                        "Addr1": "7th block, kuvempu layout",
                        "Addr2": "kuvempu layout",
                        "Loc": "Banagalore",
                        "Pin": 562160,
                        "Stcd": "29"
                    },
                    "ShipDtls": {
                        "Gstin": "29AWGPV7107B1Z1",
                        "LglNm": "CBE company pvt ltd",
                        "TrdNm": "kuvempu layout",
                        "Addr1": "7th block, kuvempu layout",
                        "Addr2": "kuvempu layout",
                        "Loc": "Banagalore",
                        "Pin": 562160,
                        "Stcd": "29"
                    },
                    "ItemList": [
                        {
                            "SlNo": "1",
                            "PrdDesc": "Rice",
                            "IsServc": "N",
                            "HsnCd": "10019920",
                            "Barcde": "123456",
                            "Qty": 100.345,
                            "FreeQty": 10,
                            "Unit": "BAG",
                            "UnitPrice": 99.545,
                            "TotAmt": 9988.84,
                            "Discount": 10,
                            "PreTaxVal": 1,
                            "AssAmt": 9978.84,
                            "GstRt": 12.0,
                            "IgstAmt": 1197.46,
                            "CgstAmt": 0,
                            "SgstAmt": 0,
                            "CesRt": 5,
                            "CesAmt": 498.94,
                            "CesNonAdvlAmt": 10,
                            "StateCesRt": 12,
                            "StateCesAmt": 1197.46,
                            "StateCesNonAdvlAmt": 5,
                            "OthChrg": 10,
                            "TotItemVal": 12897.7,
                            "OrdLineRef": "3256",
                            "OrgCntry": "AG",
                            "PrdSlNo": "12345",
                            "BchDtls": {
                                "Nm": "123456",
                                "ExpDt": "04/04/2022",
                                "WrDt": "04/04/2022"
                            },
                            "AttribDtls": [
                                {
                                    "Nm": "Rice",
                                    "Val": "10000"
                                }
                            ]
                        }
                    ],
                    "ValDtls": {
                        "AssVal": 9978.84,
                        "CgstVal": 0,
                        "SgstVal": 0,
                        "IgstVal": 1197.46,
                        "CesVal": 508.94,
                        "StCesVal": 1202.46,
                        "Discount": 10,
                        "OthChrg": 20,
                        "RndOffAmt": 0.3,
                        "TotInvVal": 12908,
                        "TotInvValFc": 12897.7
                    },
                    "PayDtls": {
                        "Nm": "ABCDE",
                        "AccDet": "5697389713210",
                        "Mode": "Cash",
                        "FinInsBr": "SBIN11000",
                        "PayTerm": "100",
                        "PayInstr": "Gift",
                        "CrTrn": "test",
                        "DirDr": "test",
                        "CrDay": 100,
                        "PaidAmt": 10000,
                        "PaymtDue": 5000
                    },
                    "RefDtls": {
                        "InvRm": "TEST",
                        "DocPerdDtls": {
                            "InvStDt": "04/04/2022",
                            "InvEndDt": "04/04/2022"
                        },
                        "PrecDocDtls": [
                            {
                                "InvNo": "DOC/0016",
                                "InvDt": "04/04/2022",
                                "OthRefNo": "123456"
                            }
                        ],
                        "ContrDtls": [
                            {
                                "RecAdvRefr": "Doc/003",
                                "RecAdvDt": "04/04/2022",
                                "TendRefr": "Abc001",
                                "ContrRefr": "Co123",
                                "ExtRefr": "Yo456",
                                "ProjRefr": "Doc-456",
                                "PORefr": "Doc-789",
                                "PORefDt": "04/04/2022"
                            }
                        ]
                    },
                    "AddlDocDtls": [
                        {
                            "Url": "https://einv-apisandbox.nic.in",
                            "Docs": "Test Doc",
                            "Info": "Document Test"
                        }
                    ],
                    "ExpDtls": {
                        "ShipBNo": "A-248",
                        "ShipBDt": "04/04/2022",
                        "Port": "INABG1",
                        "RefClm": "N",
                        "ForCur": "AED",
                        "CntCode": "AE"
                    },
                    "EwbDtls": {
                        "TransId": "12AWGPV7107B1Z1",
                        "TransName": "XYZ EXPORTS",
                        "Distance": 100,
                        "TransDocNo": "DOC01",
                        "TransDocDt": "04/04/2022",
                        "VehNo": "ka123456",
                        "VehType": "R",
                        "TransMode": "1"
                    }
                }
            }
        ]
        try:
            req = requests.put(url, data=json.dumps(formated_original), headers=headers, timeout=50)
            req.raise_for_status()
            content = req.json()
            print(content)
            print(content[0]['govt_response']['Irn'])

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

            else:
                self.Irn = False
                self.govt_log = content[0]['govt_response']['ErrorDetails']['error_message']
            # self.irn = content[0]['govt_response']['Irn'] if content[0]['govt_response']['Success'] == 'Y' else False
            self.log = content[0]['document_status']
            # self.govt_log = content[0]['govt_response']['s']
            self.AckNo = content[0]['govt_response']['AckNo']
            self.AckDt = content[0]['govt_response']['AckDt']
            self.EwbNo = content[0]['govt_response']['EwbNo']
            self.EwbDt = content[0]['govt_response']['EwbDt']
            self.EwbValidTill = content[0]['govt_response']['EwbValidTill']
            self.Success = content[0]['govt_response']['Success']
            self.SignedInvoice = content[0]['govt_response']['SignedInvoice']



        except IOError:
            error_msg = _("Required Fields Missing or Invalid Format For IRN generation.")
            raise self.env['res.config.settings'].get_config_warning(error_msg)
