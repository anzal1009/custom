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



    def action_generate_eway(self, null=None):

        comp_gstin = self.warehouse_id.partner_id.vat

        #   Testing Credentials

        company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
        if (comp_gstin == "32AAACE6765D1ZX"):
            company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
            company_gstin = "32AAACE6765D1ZX"

        #  Production Credentials

        # company_auth_token = "1.57ed9a8b-b597-41d5-89f2-81086db2c327_abdbe987b4f20506778017c6e1bc8d7c3b06547fc4de158b14eeb57f5a2bf2e4"
        # if (comp_gstin == "32AAACE6765D1ZX"):
        #     company_owner_id = "49233995-7680-4fbb-ad7d-95766ea24505"
        #     company_gstin = "32AAACE6765D1ZX"
        #
        # elif (comp_gstin == "33AAACE6765D1ZV"):
        #     company_owner_id = "b2c91294-cd23-4218-9352-35d119e556c4"
        #     company_gstin = "33AAACE6765D1ZV"
        #
        # elif (comp_gstin == "29AAACE6765D1ZK"):
        #     company_owner_id = "e7b097d9-4091-45b3-9e45-d4909b977ed3"
        #     company_gstin = "29AAACE6765D1ZK"
        #
        # elif (comp_gstin == "27AAACE6765D2ZN"):
        #     company_owner_id = "1323721e-7aab-4461-84af-b698f433ad99"
        #     company_gstin = "27AAACE6765D2ZN"

        else:
            error_msg = _("Please Check the GST Details")
            raise self.env['res.config.settings'].get_config_warning(error_msg)

        sample_str =  self.warehouse_id.partner_id.vat
        disstc = sample_str[0:2]
        print(disstc)

        sampl_str = self.partner_id.vat
        Stcd = sampl_str[0:2]
        print(Stcd)

        testeddate = self.TransDocDt
        transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

        if self.move_type == "out_invoice":
            if self.Irn:

                ########################################## If Courier Service ################################

                # if self.TransId:
                if self.transgst:

                    # url = "https://api-sandbox.clear.in/einv/v2/eInvoice/ewaybill"
                    url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/ewaybill"
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
                if self.deliver_to:

                    sample_str = self.partner_id.vat
                    disstc = sample_str[0:2]
                    print(disstc)

                    sampl_str = self.deliver_to.vat
                    Stcd = sampl_str[0:2]
                    print(Stcd)

                    # sampl_str = self.deliver_to.vat
                    # Stcd = sampl_str[0:2]
                    # print(Stcd)

                    # url = "https://api-sandbox.clear.in/einv/v2/eInvoice/ewaybill"
                    url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/ewaybill"
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
                            "VehNo": self.vehicle_no,
                            "VehType": self.VehType,
                            "ExpShipDtls": {
                                "Addr1": self.deliver_to.street or self.partner_id.street or False,
                                "Addr2": self.deliver_to.street2 or self.partner_id.street2 or False,
                                "Loc": self.deliver_to.street2 or self.partner_id.street2 or False,
                                "Pin": self.deliver_to.zip or self.partner_id.zip or False,
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
                            "VehNo": self.vehicle_no,
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
                if self.move_type == "out_invoice":

#                     company_owner_id = "853ad3de-eff3-478b-a07e-31e2c69b8486"
#                     company_auth_token = "1.19c9de17-612d-445f-bf81-fb237dec01fc_99009f9d036b2b7b3bd04c3a59f0a7662f7c9e787edfe10271ad31a78be1e286"
#                     company_gstin = "32AAACE6765D1ZX"

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

                    sample_str = self.warehouse_id.partner_id.vat
                    disstc = sample_str[0:2]

                    sampl_str = self.partner_id.vat
                    Stcd = sampl_str[0:2]

                    if self.transgst:
                        trsportgst = self.transgst
                    else:
                        trsportgst = self.partner_id.vat

                    testeddate = self.TransDocDt
                    transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

                    # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
                    url = "https://einvoicing.internal.cleartax.co/v3/ewaybill/generate"
                    # url = "https://api-sandbox.clear.in/einv/v3/ewaybill/generate"
#                     url = "https://api-einv.cleartax.in/einv/v3/ewaybill/generate"
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

                                "Gstin": self.warehouse_id.partner_id.vat,
                                "LglNm": self.warehouse_id.partner_id.name,
                                "TrdNm": self.warehouse_id.partner_id.name,
                                "Addr1": self.warehouse_id.partner_id.street,
                                "Addr2": self.warehouse_id.partner_id.street2,
                                "Loc": self.warehouse_id.partner_id.city,
                                "Pin": self.warehouse_id.partner_id.zip,
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
#                             "TransId": trsportgst,
                            "TransName": "TRANSPORT",
                            "TransMode": self.TransMode,
#                             "Distance": self.Distance,
                            "VehNo": self.vehicle_no,
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

                sample_str = self.partner_id.vat
                disstc = sample_str[0:2]

                sampl_str = self.warehouse_id.partner_id.vat
                Stcd = sampl_str[0:2]

                if self.transgst:
                    trsportgst = self.transgst
                else:
                    trsportgst = self.partner_id.vat

                testeddate = self.TransDocDt
                transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

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
                            "Gstin": self.warehouse_id.partner_id.vat,
                            "LglNm": self.warehouse_id.partner_id.name,
                            "TrdNm": self.warehouse_id.partner_id.name,
                            "Addr1": self.warehouse_id.partner_id.street,
                            "Addr2": self.warehouse_id.partner_id.street2,
                            "Loc": self.warehouse_id.partner_id.city,
                            "Pin": self.warehouse_id.partner_id.zip,
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
#                         "TransId": trsportgst,
                        "TransName": "TRANSPORT",
                        "TransMode": self.TransMode,
#                         "Distance": self.Distance,
                        "VehNo": self.vehicle_no,
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

                sample_str = self.partner_id.vat
                disstc = sample_str[0:2]

                sampl_str = self.warehouse_id.partner_id.vat
                Stcd = sampl_str[0:2]

                if self.transgst:
                    trsportgst = self.transgst
                else:
                    trsportgst = self.partner_id.vat

                testeddate = self.TransDocDt
                transportdate = datetime.strftime(testeddate, '%d/%m/%Y')

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
                            "Gstin": self.warehouse_id.partner_id.vat,
                            "LglNm": self.warehouse_id.partner_id.name,
                            "TrdNm": self.warehouse_id.partner_id.name,
                            "Addr1": self.warehouse_id.partner_id.street,
                            "Addr2": self.warehouse_id.partner_id.street2,
                            "Loc": self.warehouse_id.partner_id.city,
                            "Pin": self.warehouse_id.partner_id.zip,
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
#                         "TransId": trsportgst,
                        "TransName": "TRANSPORT",
                        "TransMode": self.TransMode,
#                         "Distance": self.Distance,
                        "VehNo": self.vehicle_no,
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


