import json
from odoo import models, _, fields
import requests
from datetime import datetime


class IrnInherit(models.Model):
    _inherit = "account.move"

    elog = fields.Char("Eway Log")
    ewb_status = fields.Char("Eway Status")
    transid = fields.Char("Transaction Id")
    transgst = fields.Char("Transporter GST")

    #
    # class EwayBillInherit(models.Model):
    #     _inherit = 'account.move'
    #
    #
    def action_generate_eway(self):

        if self.ShipBDt:

            sample_str = self.company_id.vat
            state_code = sample_str[0:2]

            sampl_str = self.partner_id.vat
            if sampl_str == "URP":
                state_code1 = 96

            else:
                state_code1 = sampl_str[0:2]

            if self.transgst:
                trsportgst = self.transgst
            else:
                trsportgst = self.partner_id.vat

            testeddate = self.TransDocDt
            transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

            if self.move_type == "out_invoice":

                # company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                # company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                # company_gstin = "32AAACE6765D1ZX"

                comp_gstin = self.company_id.vat

                #         Clear Tax Credentials for Production

                company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                if (comp_gstin == "32AAACE6765D1ZX"):
                    company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                    company_gstin = "32AAACE6765D1ZX"

                #                     company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
                #                     if (comp_gstin == "32AACCE3723D1ZB"):
                #                         company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
                #                         company_gstin = "32AACCE3723D1ZB"

                elif (comp_gstin == "33AACCE3723D1Z9"):
                    company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                    company_gstin = "33AACCE3723D1Z9"

                else:
                    error_msg = _("Please Check the GST Details")
                    raise self.env['res.config.settings'].get_config_warning(error_msg)

                sample_str = self.company_id.vat
                disstc = sample_str[0:2]

                sampl_str = self.partner_id.vat
                Stcd = sampl_str[0:2]

                testeddate = self.TransDocDt
                transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

                # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                # url = "https://einvoicing.internal.cleartax.co/v3/ewaybill/generate"
                url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                # url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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

                for items in self.invoice_line_ids:

                    inr_cost = items.cost_in_inr_cur / items.quantity
                    price = int(inr_cost)

                    print(items.tax_ids.amount)
                    GstRt = 0.0
                    iGstRt = 0.0
                    SgstAmt = 0.0
                    CgstAmt = 0.0
                    IgstAmt = 0.0

                    if items.tax_ids.name.startswith('GST'):
                        GstRt = items.tax_ids.amount
                        GstAmt = (((items.quantity * price) - (
                                (items.quantity * price) * (
                                items.discount / 100))) * items.tax_ids.amount) / 100
                        IgstAmt = 0.0
                        CgstAmt = (GstAmt / 2)
                        SgstAmt = (GstAmt / 2)

                    elif items.tax_ids.name.startswith('IGST'):
                        iGstRt = items.tax_ids.amount
                        GstAmt = (((items.quantity * price) - (
                                (items.quantity * price) * (
                                items.discount / 100))) * items.tax_ids.amount) / 100
                        IgstAmt = GstAmt
                        CgstAmt = 0.0
                        SgstAmt = 0.0

                    total = (items.quantity * price) - ((items.quantity * price) * (
                            items.discount / 100)) + GstAmt

                    item_dict = {
                        "SlNo": count,
                        "ProdName": items.name,
                        "PrdDesc": items.name,
                        #                 "IsServc": "Y",
                        # "IsServc": "N",
                        "HsnCd": items.product_id.l10n_in_hsn_code,
                        "Qty": items.quantity,
                        #                 "Unit": items.product_id.uom_id.name,
                        "Unit": "NOS",
                        "UnitPrice": price,
                        "TotAmt": items.quantity * price,
                        "Discount": (items.quantity * price) * (items.discount / 100),
                        "AssAmt": (items.quantity * price) - (
                                (items.quantity * price) * (items.discount / 100)),
                        # "GstRt": GstRt,
                        "CgstRt": GstRt / 2,
                        "SgstRt": GstRt / 2,
                        "IgstRt": iGstRt,
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

                    #                     print(items.tax_ids.amount)
                    #                     GstRt = 0.0
                    #                     iGstRt = 0.0
                    #                     SgstAmt = 0.0
                    #                     CgstAmt = 0.0
                    #                     IgstAmt = 0.0

                    #                     if items.tax_ids.name.startswith('GST'):
                    #                         GstRt = items.tax_ids.amount
                    #                         GstAmt = (((items.quantity * items.price_unit) - (
                    #                                 (items.quantity * items.price_unit) * (
                    #                                 items.discount / 100))) * items.tax_ids.amount) / 100
                    #                         IgstAmt = 0.0
                    #                         CgstAmt = (GstAmt / 2)
                    #                         SgstAmt = (GstAmt / 2)

                    #                     elif items.tax_ids.name.startswith('IGST'):
                    #                         iGstRt = items.tax_ids.amount
                    #                         GstAmt = (((items.quantity * items.price_unit) - (
                    #                                 (items.quantity * items.price_unit) * (
                    #                                 items.discount / 100))) * items.tax_ids.amount) / 100
                    #                         IgstAmt = GstAmt
                    #                         CgstAmt = 0.0
                    #                         SgstAmt = 0.0

                    #                     total = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                    #                             items.discount / 100)) + GstAmt

                    #                     item_dict = {
                    #                         "SlNo": count,
                    #                         "ProdName": items.name,
                    #                         "PrdDesc": items.name,
                    #                         #                 "IsServc": "Y",
                    #                         # "IsServc": "N",
                    #                         "HsnCd": items.product_id.l10n_in_hsn_code,
                    #                         "Qty": items.quantity,
                    #                         #                 "Unit": items.product_id.uom_id.name,
                    #                         "Unit": "NOS",
                    #                         # "UnitPrice": items.price_unit,
                    #                         # "TotAmt": items.quantity * items.price_unit,
                    #                         # "Discount": (items.quantity * items.price_unit) * (items.discount / 100),
                    #                         "AssAmt": (items.quantity * items.price_unit) - (
                    #                                 (items.quantity * items.price_unit) * (items.discount / 100)),
                    #                         # "GstRt": GstRt,
                    #                         "CgstRt": GstRt / 2,
                    #                         "SgstRt": GstRt / 2,
                    #                         "IgstRt": iGstRt,
                    #                         "IgstAmt": IgstAmt,
                    #                         "CgstAmt": CgstAmt,
                    #                         "SgstAmt": SgstAmt,
                    #                         "TotItemVal": total,
                    #                     }
                    #                     count = count + 1
                    #                     TotalAssVal = TotalAssVal + ((items.quantity * items.price_unit) - (
                    #                             (items.quantity * items.price_unit) * (items.discount / 100)))
                    #                     TotalCgstVal = TotalCgstVal + CgstAmt
                    #                     TotalSgstVal = TotalSgstVal + CgstAmt
                    #                     TotalIgstVal = TotalIgstVal + IgstAmt
                    #                     TotInvVal = TotInvVal + total
                    #                     item_list.append(item_dict)

                    inv_date = self.invoice_date
                    doc_date = datetime.strftime(testeddate, '%d/%m/%Y')

                    invoice = {
                        "DocumentNumber": self.name,
                        "DocumentType": "INV",
                        "DocumentDate": doc_date,
                        "SupplyType": "OUTWARD",
                        "SubSupplyType": "Export",
                        "SubSupplyTypeDesc": "Others",
                        "TransactionType": "Bill to-ship to",
                        # "TransactionType": "Combination",
                        # "TransactionType": "Bill From-Dispatch From",
                        # "TransactionType": "Regular",

                        # customer (to billing)
                        "BuyerDtls": {
                            "Gstin": self.partner_id.vat,
                            "LglNm": self.partner_id.name,
                            "TrdNm": self.partner_id.name,
                            "Addr1": self.partner_id.street,
                            "Addr2": self.partner_id.street2,
                            "Loc": self.partner_id.city,
                            # "Pin": self.partner_id.zip,
                            "Stcd": "99",
                        },
                        # supplier (from billing)
                        "SellerDtls": {
                            "Gstin": self.company_id.vat,
                            "LglNm": self.company_id.name,
                            "TrdNm": self.company_id.name,
                            "Addr1": self.company_id.street,
                            "Addr2": self.company_id.street2,
                            "Loc": self.company_id.city,
                            "Pin": self.company_id.zip,
                            "Stcd": disstc,
                        },
                        # shipping (to shipping)
                        "ExpShipDtls": {
                            "LglNm": self.company_id.name,
                            "Addr1": self.company_id.street,
                            "Loc": self.company_id.city,
                            "Pin": self.company_id.zip,
                            "Stcd": disstc,
                        },
                        # dispatch (from shipping)
                        "DispDtls": {
                            "Nm": self.partner_id.name,
                            "Addr1": self.partner_id.street,
                            "Addr2": self.partner_id.street2,
                            "Loc": self.partner_id.city,
                            "Pin": 686673,
                            "Stcd": "32"
                        },

                        # invoice = {
                        #     "DocumentNumber": self.name,
                        #     "DocumentType": "INV",
                        #     "DocumentDate": doc_date,
                        #     "SupplyType": "OUTWARD",
                        #     "SubSupplyType": "Export",
                        #     "SubSupplyTypeDesc": "Others",
                        #     "TransactionType": "Bill to-ship to",
                        #     # "TransactionType": "Combination",
                        #     # "TransactionType": "Bill From-Dispatch From",
                        #     # "TransactionType": "Regular",
                        #
                        #     #customer (to billing)
                        #     "BuyerDtls": {
                        #         "Gstin": self.partner_id.vat,
                        #         "LglNm": self.partner_id.name,
                        #         "TrdNm": self.partner_id.name,
                        #         "Addr1": self.partner_id.street,
                        #         "Addr2": self.partner_id.street2,
                        #         "Loc": self.partner_id.city,
                        #         # "Pin": self.partner_id.zip,
                        #         "Stcd": "99",
                        #     },
                        #     # supplier (from billing)
                        #     "SellerDtls": {
                        #         "Gstin": self.company_id.vat,
                        #         "LglNm": self.company_id.name,
                        #         "TrdNm": self.company_id.name,
                        #         "Addr1": self.company_id.street,
                        #         "Addr2": self.company_id.street2,
                        #         "Loc": self.company_id.city,
                        #         "Pin": self.company_id.zip,
                        #         "Stcd": disstc,
                        #     },
                        #     # shipping (to shipping)
                        #     "ExpShipDtls": {
                        #         "LglNm": self.partner_id.name,
                        #         "Addr1":self.partner_id.street,
                        #         "Loc": self.partner_id.city,
                        #         "Pin": self.partner_id.zip,
                        #         "Stcd": "96",
                        #     },
                        #     # dispatch (from shipping)
                        #     "DispDtls": {
                        #         "Nm": "ARUN STEELS",
                        #         "Addr1": "322 & 323 THIRUVALLUVAR NAGAR NEELI",
                        #         "Addr2": "COIMBATORE",
                        #         "Loc": "COIMBATORE",
                        #         "Pin": 641033,
                        #         "Stcd": "33"
                        #     },

                        # "DispDtls": {
                        #     "Nm": self.partner_id.name,
                        #     "Addr1": self.partner_id.street,
                        #     "Addr2": self.partner_id.street2,
                        #     "Loc": self.partner_id.city,
                        #     "Pin": 686673,
                        #     "Stcd": "32",
                        # },
                        # "ExpShipDtls": {
                        #     "LglNm": "ARUN STEELS",
                        #     "Addr1": "322 & 323 THIRUVALLUVAR NAGAR NEELI",
                        #     "Loc": "COIMBATORE",
                        #     "Pin": 641033,
                        #     "Stcd": "33"
                        # },

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
                        "TransId": self.company_id.vat,
                        "TransName": "TRANSPORT",
                        "TransMode": self.TransMode,
                        "Distance": self.Distance,
                        "VehNo": self.VehNo,
                        "VehType": None
                    }

                    print(invoice)

                    try:
                        req = requests.put(url, data=json.dumps(invoice), headers=headers, timeout=50)
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
        else:

            if self.Irn:
                # raise self.env['res.config.settings'].get_config_warning("Generate IRN First")

                # Clear Tax Sandbox Credentials for Testing
                comp_gstin = self.company_id.vat

                #         Clear Tax Credentials for Production

                company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                if (comp_gstin == "32AAACE6765D1ZX"):
                    company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                    company_gstin = "32AAACE6765D1ZX"

                #                 company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
                #                 if (comp_gstin == "32AACCE3723D1ZB"):
                #                     company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
                #                     company_gstin = "32AACCE3723D1ZB"

                elif (comp_gstin == "33AACCE3723D1Z9"):
                    company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                    company_gstin = "33AACCE3723D1Z9"

                else:
                    error_msg = _("Please Check the GST Details")
                    raise self.env['res.config.settings'].get_config_warning(error_msg)

                # company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                # company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                # company_gstin = "32AAACE6765D1ZX"

                sample_str = self.company_id.vat
                disstc = sample_str[0:2]
                print(disstc)

                sampl_str = self.partner_id.vat
                Stcd = sampl_str[0:2]
                print(Stcd)

                if self.transgst:
                    trsportgst = self.transgst
                # else:
                #     trsportgst = self.partner_id.vat

                testeddate = self.TransDocDt
                transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

                ########################################## If Courier Service ################################

                # if self.TransId:
                if self.transgst:

                    # url = "https://api-sandbox.clear.in/einv/v2/eInvoice/ewaybill"
                    url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/ewaybill"
                    # url = "https://api-einv.cleartax.in/v2/eInvoice/ewaybill"
                    #         url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
                    headers = {"Content-type": "application/json",
                               "x-cleartax-auth-token": company_auth_token,
                               "x-cleartax-product": "EInvoice", "owner_id": company_owner_id,
                               "gstin": company_gstin}

                    data5 = [
                        {
                            "Irn": self.Irn,
                            # "Distance": self.Distance,
                            # "TransMode": self.TransMode,
                            "TransId": self.transgst,
                            "TransName": self.TransName,

                        }]
                    try:
                        req = requests.post(url, data=json.dumps(data5), headers=headers, timeout=50)
                        req.raise_for_status()
                        content = req.json()
                        print(content[0]['govt_response'])

                        if content[0]['govt_response']['Success'] == 'Y':
                            # self.Irn = content[0]['govt_response']['Irn'] if content[0]['govt_response'][
                            #                                                      'Success'] == 'Y' else False
                            self.Status = content[0]['govt_response']['Success']
                            self.ewb_status = content[0]['ewb_status']
                            #     # self.AckNo = content[0]['govt_response']['AckNo']
                            #     # self.AckDt = content[0]['govt_response']['AckDt']
                            self.EwbNo = content[0]['govt_response']['EwbNo']
                            self.EwbDt = content[0]['govt_response']['EwbDt']
                            # self.EwbValidTill = content[0]['govt_response']['EwbValidTill']
                            self.elog = content[0]['govt_response']['Success']
                            # self.Status = content[0]['govt_response']['Success']
                        #     # self.SignedInvoice = content[0]['govt_response']['SignedInvoice']
                        #
                        else:
                            self.EwbNo = False
                            self.elog = content[0]['govt_response']['ErrorDetails']
                            # self.ewb_status = content[0]['ewb_status'] or "Not Applicable"

                    except IOError:
                        error_msg = _("Required Fields Missing or Invalid Format For EWAY generation.")
                        raise self.env['res.config.settings'].get_config_warning(error_msg)

                ####################################### If DELIVERY Address ################################

                #                 if self.partner_shipping_id:
                elif self.partner_id != self.partner_shipping_id:

                    sample_str = self.partner_id.vat
                    disstc = sample_str[0:2]
                    print(disstc)

                    sampl_str = self.partner_shipping_id.vat
                    Stcd = sampl_str[0:2]
                    print(Stcd)

                    # sampl_str = self.deliver_to.vat
                    # Stcd = sampl_str[0:2]
                    # print(Stcd)

                    # url = "https://api-sandbox.clear.in/einv/v2/eInvoice/ewaybill"
                    url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/ewaybill"
                    # url = "https://api-einv.cleartax.in/v2/eInvoice/ewaybill"
                    #         url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
                    headers = {"Content-type": "application/json",
                               "x-cleartax-auth-token": company_auth_token,
                               "x-cleartax-product": "EInvoice", "owner_id": company_owner_id,
                               "gstin": company_gstin}

                    data6 = [
                        {
                            "Irn": self.Irn,
                            #                         "Distance": self.Distance,
                            "TransMode": self.TransMode,
                            #                         "TransId": self.transgst,
                            #                         "TransName": self.TransName,
                            "TransDocDt": transportdate,
                            #                         "TransDocNo": self.TransDocNo,
                            "VehNo": self.VehNo,
                            "VehType": self.VehType,
                            "ExpShipDtls": {
                                "Addr1": self.partner_shipping_id.street or self.partner_id.street or False,
                                "Addr2": self.partner_shipping_id.street2 or self.partner_id.street2 or False,
                                "Loc": self.partner_shipping_id.street2 or self.partner_id.street2 or False,
                                "Pin": self.partner_shipping_id.zip or self.partner_id.zip or False,
                                "Stcd": Stcd
                            },

                            #                             "ExpShipDtls": {
                            #                                 "Addr1": self.partner_shipping_id.street or self.partner_id.street or False,
                            #                                 "Addr2": self.partner_shipping_id.street2 or self.partner_id.street2 or False,
                            #                                 "Loc": self.partner_shipping_id.street2 or self.partner_id.street2 or False,
                            #                                 "Pin": self.partner_shipping_id.zip or self.partner_id.zip or False,
                            #                                 "Stcd": Stcd
                            #                             },
                            # "DispDtls": {
                            #     "Nm": self.partner_id.name,
                            #     "Addr1": self.partner_id.street,
                            #     "Addr2": self.partner_id.street2,
                            #     "Loc": self.partner_id.city,
                            #     "Pin": self.partner_id.zip,
                            #     "Stcd": disstc
                            # }
                        }]
                    try:
                        req = requests.post(url, data=json.dumps(data6), headers=headers, timeout=50)
                        req.raise_for_status()
                        content = req.json()
                        print(content[0]['govt_response'])

                        if content[0]['govt_response']['Success'] == 'Y':
                            # self.Irn = content[0]['govt_response']['Irn'] if content[0]['govt_response'][
                            #                                                      'Success'] == 'Y' else False
                            self.Status = content[0]['govt_response']['Success']
                            self.ewb_status = content[0]['ewb_status']
                            #     # self.AckNo = content[0]['govt_response']['AckNo']
                            #     # self.AckDt = content[0]['govt_response']['AckDt']
                            self.EwbNo = content[0]['govt_response']['EwbNo']
                            self.EwbDt = content[0]['govt_response']['EwbDt']
                            self.EwbValidTill = content[0]['govt_response']['EwbValidTill']
                            self.elog = content[0]['govt_response']['Success']
                            # self.Status = content[0]['govt_response']['Success']
                        #     # self.SignedInvoice = content[0]['govt_response']['SignedInvoice']
                        #
                        else:
                            self.EwbNo = False
                            self.elog = content[0]['govt_response']['ErrorDetails']
                            # self.ewb_status = content[0]['ewb_status'] or "Not Applicable"

                    except IOError:
                        error_msg = _("Required Fields Missing or Invalid Format For EWAY generation.")
                        raise self.env['res.config.settings'].get_config_warning(error_msg)

                #################### E way For REGULAR ###############

                else:
                    # url = "https://api-sandbox.clear.in/einv/v2/eInvoice/ewaybill"
                    url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/ewaybill"
                    # url = "https://api-einv.cleartax.in/v2/eInvoice/ewaybill"
                    #         url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
                    headers = {"Content-type": "application/json",
                               "x-cleartax-auth-token": company_auth_token,
                               "x-cleartax-product": "EInvoice", "owner_id": company_owner_id,
                               "gstin": company_gstin}

                    data1 = [
                        {
                            "Irn": self.Irn,
                            #                         "Distance": self.Distance,
                            "TransMode": self.TransMode,
                            #                         "TransId": self.transgst,
                            #                         "TransName": self.TransName,
                            "TransDocDt": transportdate,
                            #                         "TransDocNo": self.TransDocNo,
                            "VehNo": self.VehNo,
                            "VehType": self.VehType,
                            # "ExpShipDtls": {
                            #     "Addr1": self.deliver_to.street or self.partner_id.street or False,
                            #     "Addr2": self.deliver_to.street2 or self.partner_id.street2 or False,
                            #     "Loc": self.deliver_to.city or self.partner_id.city or False,
                            #     "Pin": self.deliver_to.zip or self.partner_id.zip or False,
                            #     "Stcd": Stcd
                            # },
                            # "DispDtls": {
                            #     "Nm": self.warehouse_id.partner_id.name,
                            #     "Addr1": self.warehouse_id.partner_id.street,
                            #     "Addr2": self.warehouse_id.partner_id.street2,
                            #     "Loc": self.warehouse_id.partner_id.city,
                            #     "Pin": self.warehouse_id.partner_id.zip,
                            #     "Stcd": disstc
                            # }
                        }]
                    try:
                        req = requests.post(url, data=json.dumps(data1), headers=headers, timeout=50)
                        req.raise_for_status()
                        content = req.json()
                        print(content[0]['govt_response'])

                        if content[0]['govt_response']['Success'] == 'Y':
                            # self.Irn = content[0]['govt_response']['Irn'] if content[0]['govt_response'][
                            #                                                      'Success'] == 'Y' else False
                            self.Status = content[0]['govt_response']['Success']
                            self.ewb_status = content[0]['ewb_status']
                            #     # self.AckNo = content[0]['govt_response']['AckNo']
                            #     # self.AckDt = content[0]['govt_response']['AckDt']
                            self.EwbNo = content[0]['govt_response']['EwbNo']
                            self.EwbDt = content[0]['govt_response']['EwbDt']
                            self.EwbValidTill = content[0]['govt_response']['EwbValidTill']
                            self.elog = content[0]['govt_response']['Success']
                            # self.Status = content[0]['govt_response']['Success']
                        #     # self.SignedInvoice = content[0]['govt_response']['SignedInvoice']
                        #
                        else:
                            self.EwbNo = False
                            self.elog = content[0]['govt_response']['ErrorDetails']
                            # self.ewb_status = content[0]['ewb_status'] or "Not Applicable"

                    except IOError:
                        error_msg = _("Required Fields Missing or Invalid Format For EWAY generation.")
                        raise self.env['res.config.settings'].get_config_warning(error_msg)




            if not self.Irn:

                if not self.TransDocDt:
                    raise self.env['res.config.settings'].get_config_warning("Enter Transportation Date")

                if self.transgst:
                    trsportgst = self.transgst
                else:
                    trsportgst = self.partner_id.vat
                print(trsportgst)

                if self.move_type == "out_invoice":

                    # company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                    # company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                    # company_gstin = "32AAACE6765D1ZX"

                    comp_gstin = self.company_id.vat

                    #         Clear Tax Credentials for Production

                    company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                    if (comp_gstin == "32AAACE6765D1ZX"):
                        company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                        company_gstin = "32AAACE6765D1ZX"

                    #                     company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
                    #                     if (comp_gstin == "32AACCE3723D1ZB"):
                    #                         company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
                    #                         company_gstin = "32AACCE3723D1ZB"

                    elif (comp_gstin == "33AACCE3723D1Z9"):
                        company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                        company_gstin = "33AACCE3723D1Z9"

                    else:
                        error_msg = _("Please Check the GST Details")
                        raise self.env['res.config.settings'].get_config_warning(error_msg)

                    sample_str = self.company_id.vat
                    disstc = sample_str[0:2]

                    sampl_str = self.partner_id.vat
                    Stcd = sampl_str[0:2]

                    testeddate = self.TransDocDt
                    transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

                    # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                    # url = "https://einvoicing.internal.cleartax.co/v3/ewaybill/generate"
                    url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                    # url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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

                    for items in self.invoice_line_ids:
                        print(items.tax_ids.amount)
                        GstRt = 0.0
                        iGstRt = 0.0
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
                            iGstRt = items.tax_ids.amount
                            GstAmt = (((items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                                    items.discount / 100))) * items.tax_ids.amount) / 100
                            IgstAmt = GstAmt
                            CgstAmt = 0.0
                            SgstAmt = 0.0

                        total = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                                items.discount / 100)) + GstAmt

                        item_dict = {
                            "SlNo": count,
                            "ProdName": items.name,
                            "PrdDesc": items.name,
                            #                 "IsServc": "Y",
                            # "IsServc": "N",
                            "HsnCd": items.product_id.l10n_in_hsn_code,
                            "Qty": items.quantity,
                            #                 "Unit": items.product_id.uom_id.name,
                            "Unit": "NOS",
                            # "UnitPrice": items.price_unit,
                            # "TotAmt": items.quantity * items.price_unit,
                            # "Discount": (items.quantity * items.price_unit) * (items.discount / 100),
                            "AssAmt": (items.quantity * items.price_unit) - (
                                    (items.quantity * items.price_unit) * (items.discount / 100)),
                            # "GstRt": GstRt,
                            "CgstRt": GstRt / 2,
                            "SgstRt": GstRt / 2,
                            "IgstRt": iGstRt,
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

                        inv_date = self.invoice_date
                        doc_date = datetime.strftime(testeddate, '%d/%m/%Y')

                        invoice = {
                            "DocumentNumber": self.name,
                            "DocumentType": "INV",
                            "DocumentDate": doc_date,
                            "SupplyType": "OUTWARD",
                            "SubSupplyType": "SUPPLY",
                            "SubSupplyTypeDesc": "Others",
                            "TransactionType": "Regular",
                            "BuyerDtls": {
                                "Gstin": self.partner_id.vat,
                                "LglNm": self.partner_id.name,
                                "TrdNm": self.partner_id.name,
                                "Addr1": self.partner_id.street,
                                "Addr2": self.partner_id.street2,
                                "Loc": self.partner_id.city,
                                "Pin": self.partner_id.zip,
                                "Stcd": Stcd,
                            },
                            "SellerDtls": {
                                "Gstin": self.company_id.vat,
                                "LglNm": self.company_id.name,
                                "TrdNm": self.company_id.name,
                                "Addr1": self.company_id.street,
                                "Addr2": self.company_id.street2,
                                "Loc": self.company_id.city,
                                "Pin": self.company_id.zip,
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

                        print(invoice)

                        try:
                            req = requests.put(url, data=json.dumps(invoice), headers=headers, timeout=50)
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

                else:

                    if self.move_type == "out_refund":

                        # company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                        # company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                        # company_gstin = "32AAACE6765D1ZX"

                        comp_gstin = self.company_id.vat

                        #         Clear Tax Credentials for Production

                        company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                        if (comp_gstin == "32AAACE6765D1ZX"):
                            company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                            company_gstin = "32AAACE6765D1ZX"

                        #                     company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
                        #                     if (comp_gstin == "32AACCE3723D1ZB"):
                        #                         company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
                        #                         company_gstin = "32AACCE3723D1ZB"

                        elif (comp_gstin == "33AACCE3723D1Z9"):
                            company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                            company_gstin = "33AACCE3723D1Z9"

                        else:
                            error_msg = _("Please Check the GST Details")
                            raise self.env['res.config.settings'].get_config_warning(error_msg)

                        sample_str = self.partner_id.vat
                        disstc = sample_str[0:2]

                        sampl_str = self.company_id.vat
                        Stcd = sampl_str[0:2]

                        if self.transgst:
                            trsportgst = self.transgst
                        else:
                            trsportgst = self.partner_id.vat

                        testeddate = self.TransDocDt
                        transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

                        # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                        # url = "https://einvoicing.internal.cleartax.co/v3/ewaybill/generate"
                        url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                        # url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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

                        for items in self.invoice_line_ids:
                            print(items.tax_ids.amount)
                            GstRt = 0.0
                            iGstRt = 0.0
                            SgstAmt = 0.0
                            CgstAmt = 0.0
                            IgstAmt = 0.0

                            if items.tax_ids.name.startswith('GST'):
                                GstRt = items.tax_ids.amount
                                GstAmt = (((items.quantity * items.price_unit) - (
                                            (items.quantity * items.price_unit) * (
                                            items.discount / 100))) * items.tax_ids.amount) / 100
                                IgstAmt = 0.0
                                CgstAmt = (GstAmt / 2)
                                SgstAmt = (GstAmt / 2)

                            elif items.tax_ids.name.startswith('IGST'):
                                iGstRt = items.tax_ids.amount
                                GstAmt = (((items.quantity * items.price_unit) - (
                                            (items.quantity * items.price_unit) * (
                                            items.discount / 100))) * items.tax_ids.amount) / 100
                                IgstAmt = GstAmt
                                CgstAmt = 0.0
                                SgstAmt = 0.0

                            total = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                                    items.discount / 100)) + GstAmt

                            item_dict = {
                                "SlNo": count,
                                "ProdName": items.name,
                                "PrdDesc": items.name,
                                #                 "IsServc": "Y",
                                # "IsServc": "N",
                                "HsnCd": items.product_id.l10n_in_hsn_code,
                                "Qty": items.quantity,
                                #                 "Unit": items.product_id.uom_id.name,
                                "Unit": "NOS",
                                # "UnitPrice": items.price_unit,
                                # "TotAmt": items.quantity * items.price_unit,
                                # "Discount": (items.quantity * items.price_unit) * (items.discount / 100),
                                "AssAmt": (items.quantity * items.price_unit) - (
                                        (items.quantity * items.price_unit) * (items.discount / 100)),
                                # "GstRt": GstRt,
                                "CgstRt": GstRt / 2,
                                "SgstRt": GstRt / 2,
                                "IgstRt": iGstRt,
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

                            inv_date = self.invoice_date
                            doc_date = datetime.strftime(testeddate, '%d/%m/%Y')

                            cust_credit = {
                                "DocumentNumber": self.name,
                                "DocumentType": "OTH",
                                "DocumentDate": doc_date,
                                "SupplyType": "INWARD",
                                "SubSupplyType": "OTH",
                                "SubSupplyTypeDesc": "Others",
                                "TransactionType": "Regular",
                                "SellerDtls": {
                                    "Gstin": self.partner_id.vat,
                                    "LglNm": self.partner_id.name,
                                    "TrdNm": self.partner_id.name,
                                    "Addr1": self.partner_id.street,
                                    "Addr2": self.partner_id.street2,
                                    "Loc": self.partner_id.city,
                                    "Pin": self.partner_id.zip,
                                    "Stcd": disstc,
                                },
                                "BuyerDtls": {
                                    "Gstin": self.company_id.vat,
                                    "LglNm": self.company_id.name,
                                    "TrdNm": self.company_id.name,
                                    "Addr1": self.company_id.street,
                                    "Addr2": self.company_id.street2,
                                    "Loc": self.company_id.city,
                                    "Pin": self.company_id.zip,
                                    "Stcd": Stcd,
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

                            print(cust_credit)

                            try:
                                req = requests.put(url, data=json.dumps(cust_credit), headers=headers, timeout=50)
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

                    if self.move_type == "in_refund":

                        # company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                        # company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                        # company_gstin = "32AAACE6765D1ZX"

                        comp_gstin = self.company_id.vat

                        #         Clear Tax Credentials for Production

                        company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
                        if (comp_gstin == "32AAACE6765D1ZX"):
                            company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
                            company_gstin = "32AAACE6765D1ZX"

                        #                     company_auth_token = "1.ca3f872d-e57a-4311-94db-85bb31897a0c_3901c0953efdcb2f9f3fdaf0018f80917d66adc3577eb6feddffd982182da682"
                        #                     if (comp_gstin == "32AACCE3723D1ZB"):
                        #                         company_owner_id = "88114c32-9194-4f8e-96d0-1d975191d800"
                        #                         company_gstin = "32AACCE3723D1ZB"

                        elif (comp_gstin == "33AACCE3723D1Z9"):
                            company_owner_id = "9ed95b39-9337-43ad-997f-4385d6fd7fe7"
                            company_gstin = "33AACCE3723D1Z9"

                        else:
                            error_msg = _("Please Check the GST Details")
                            raise self.env['res.config.settings'].get_config_warning(error_msg)

                        sample_str = self.partner_id.vat
                        disstc = sample_str[0:2]

                        sampl_str = self.company_id.vat
                        Stcd = sampl_str[0:2]

                        if self.transgst:
                            trsportgst = self.transgst
                        else:
                            trsportgst = self.partner_id.vat

                        testeddate = self.TransDocDt
                        transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

                        # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                        # url = "https://einvoicing.internal.cleartax.co/v3/ewaybill/generate"
                        url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                        # url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
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

                        for items in self.invoice_line_ids:
                            print(items.tax_ids.amount)
                            GstRt = 0.0
                            iGstRt = 0.0
                            SgstAmt = 0.0
                            CgstAmt = 0.0
                            IgstAmt = 0.0

                            if items.tax_ids.name.startswith('GST'):
                                GstRt = items.tax_ids.amount
                                GstAmt = (((items.quantity * items.price_unit) - (
                                            (items.quantity * items.price_unit) * (
                                            items.discount / 100))) * items.tax_ids.amount) / 100
                                IgstAmt = 0.0
                                CgstAmt = (GstAmt / 2)
                                SgstAmt = (GstAmt / 2)

                            elif items.tax_ids.name.startswith('IGST'):
                                iGstRt = items.tax_ids.amount
                                GstAmt = (((items.quantity * items.price_unit) - (
                                            (items.quantity * items.price_unit) * (
                                            items.discount / 100))) * items.tax_ids.amount) / 100
                                IgstAmt = GstAmt
                                CgstAmt = 0.0
                                SgstAmt = 0.0

                            total = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (
                                    items.discount / 100)) + GstAmt

                            item_dict = {
                                "SlNo": count,
                                "ProdName": items.name,
                                "PrdDesc": items.name,
                                #                 "IsServc": "Y",
                                # "IsServc": "N",
                                "HsnCd": items.product_id.l10n_in_hsn_code,
                                "Qty": items.quantity,
                                #                 "Unit": items.product_id.uom_id.name,
                                "Unit": "NOS",
                                # "UnitPrice": items.price_unit,
                                # "TotAmt": items.quantity * items.price_unit,
                                # "Discount": (items.quantity * items.price_unit) * (items.discount / 100),
                                "AssAmt": (items.quantity * items.price_unit) - (
                                        (items.quantity * items.price_unit) * (items.discount / 100)),
                                # "GstRt": GstRt,
                                "CgstRt": GstRt / 2,
                                "SgstRt": GstRt / 2,
                                "IgstRt": iGstRt,
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

                            inv_date = self.invoice_date
                            doc_date = datetime.strftime(testeddate, '%d/%m/%Y')

                            vendor_credit = {
                                "DocumentNumber": self.name,
                                "DocumentType": "INV",
                                "DocumentDate": doc_date,
                                "SupplyType": "OUTWARD",
                                "SubSupplyType": "SUPPLY",
                                "SubSupplyTypeDesc": "Others",
                                "TransactionType": "Regular",
                                "BuyerDtls": {
                                    "Gstin": self.partner_id.vat,
                                    "LglNm": self.partner_id.name,
                                    "TrdNm": self.partner_id.name,
                                    "Addr1": self.partner_id.street,
                                    "Addr2": self.partner_id.street2,
                                    "Loc": self.partner_id.city,
                                    "Pin": self.partner_id.zip,
                                    "Stcd": disstc,
                                },
                                "SellerDtls": {
                                    "Gstin": self.company_id.vat,
                                    "LglNm": self.company_id.name,
                                    "TrdNm": self.company_id.name,
                                    "Addr1": self.company_id.street,
                                    "Addr2": self.company_id.street2,
                                    "Loc": self.company_id.city,
                                    "Pin": self.company_id.zip,
                                    "Stcd": Stcd,
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

                            try:
                                req = requests.put(url, data=json.dumps(vendor_credit), headers=headers, timeout=50)
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
