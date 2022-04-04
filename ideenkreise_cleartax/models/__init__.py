from odoo import api, models, fields, _
import requests
import json
import qrcode
import base64


class SaleOrderInherit(models.Model):
    _inherit = 'account.move'


    # def action_generate_irn(self):
    #     print('hello')

    def action_generate_irn(self):
        print(self, "generate_irn")
        url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/generate"
        headers = {"Content-type": "application/json",
                   "x-cleartax-auth-token": "1.76c8055b-687c-4563-87bf-4bcff17081c8_9ce29420ba9a947b529b2d81c44e7cee949fdeae1971920b17438ddd425ddf94",
                   "x-cleartax-product": "EInvoice", "owner_id": "5b664f35-4214-46ed-84c8-4f30fabc9cba",
                   "gstin": "29AAFCD5862R000"}
        item_list = []
        count = 1
        # itemamtsum = 0
        # gstamtsum = 0
        # AssVal = 0
        # IgstVal = 0
        # Discount = 0
        # TotInvVal = 0

        for items in self.invoice_line_ids:
            print(items.tax_ids.name)
            # def find_tax(self):
            # if items.tax_ids.name.startswith('GST'):
            #     CGST = items.quantity * items.price_unit,
            #     SGST = (items.quantity * items.price_unit) * (items.discount / 100)
            #
            #     # if ('GST 5%') == items.tax_ids.name:
            #     #     print('cgst')
            # elif items.tax_ids.name.startswith('IGST'):
            #     # IGST_amt = (items.quantity * items.price_unit) - ((items.quantity * items.price_unit) * (items.discount / 100))
            #      print('ooo')
            # if items.tax_ids.name == "GST":
            #     GstRt=items.quantity * items.price_unit
            #     SgstAmt=(items.quantity * items.price_unit) * (items.discount / 100)
            #     CgstAmt= items.product_id.uom_id.name
            #     if items.tax_ids.name == "IGST":
            #         GstRt=  (items.quantity * items.price_unit) - (
            #                 (items.quantity * items.price_unit) * (items.discount / 100))
            #         IgstAmt= items.quantity
            #


                # GstRt: items.gstrate
                # SgstAmt: items.sgstamount
                # CgstAmt: items.cgstamount
                # if items.tax_ids.name == "IGST":
                #     GstRt: items.gstrate
                #     IgstAmt: items.igstamount

            GstRt=0.0
            CgstAmt=0.0
            IgstAmt=0.0
            if items.tax_ids.name.startswith('GST'):
                GstRt=items.quantity * items.price_unit
                CgstAmt=items.quantity
                print("pppp")
            elif items.tax_ids.name.startswith('IGST'):
                IgstAmt=(items.quantity * items.price_unit) * (items.discount / 100)
                print('oo')

            # discount = 10 *
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
                "IgstAmt":IgstAmt,
                "CgstAmt":CgstAmt,

                # "cst":IGST_amt,
                #
                #     "TotItemVal": items.amount_residual,

            }

            count = count + 1
            item_list.append(item_dict)
            print(item_list)
        #
        #     AssVal = AssVal + items.itemtaxablevalue
        #     IgstVal = IgstVal + items.igstamount
        #     Discount = Discount + items.itemdiscountamount
        #     TotInvVal = TotInvVal + items.itemtotalamount
        #
        #     itemamtsum = itemamtsum + items.itemtaxablevalue
        #     gstamtsum = gstamtsum + items.igstamount
        #     total_invoice_value = items.itemtotalamount + items.totaltaxablevalue

        # formated_original = [
        #     {
        #         "transaction": {
        #             "Version": "1.1",
        #             "TranDtls": {
        #                 "TaxSch": "GST",
        #                 "SupTyp": "EXPWP",
        #                 "EcmGstin": None,
        #                 "IgstOnIntra": "N"
        #             },
        #             "DocDtls": {
        #                 "Typ": "INV",
        #                 "No": "2022900765",
        #                 "Dt": "01/04/2022"
        #             },
        #             "SellerDtls": {
        #                 "Gstin": "29AAFCD5862R000",
        #                 "LglNm": "Eastern Condiments Pvt. Ltd",
        #                 "TrdNm": "Eastern Condiments Pvt. Ltd",
        #                 "Addr1": "Branch Code:7IV/1D,IV/1EIRUMALAPADY,PANIPRA P.O.,KOTHAMANGALAM, ERNAKULAM,",
        #                 "Loc": "Eranakulam",
        #                 "Pin": "562160",
        #                 "Stcd": "29",
        #             },
        #             "BuyerDtls": {
        #                 "Gstin": "URP",
        #                 "LglNm": "JALEEL DISTRIBUTION LLC",
        #                 "TrdNm": "JALEEL DISTRIBUTION LLC",
        #                 "Pos": "96",
        #                 "Addr1": "P.O.BOX NO : 3262  DUBAI, UNITED ARAB EMIRATES Tel .NO :009714-3339191",
        #                 "Loc": "DUBAI",
        #                 "Pin": "999999",
        #                 "Stcd": "96"
        #             },
        #             "ShipDtls": {
        #                 "Gstin": "URP",
        #                 "LglNm": "India Gateway Terminal Private Limited",
        #                 "TrdNm": "India Gateway Terminal Private Limited",
        #                 "Addr1": "Administration Building, ICTT,",
        #                 "Addr2": "Vallarpadam SEZ, Mulavukadu Village",
        #                 "Loc": "Ernakulam",
        #                 "Pin": 562160,
        #                 "Stcd": 29
        #             },
        #             "ItemList": [
        #                 {
        #                     "SlNo": 1,
        #                     "PrdDesc": "Hs Code -15131900- 67/12- Coconut Oil 2 Ltr Coconut Oil Bottle",
        #                     "IsServc": "N",
        #                     "HsnCd": "15131900",
        #                     "Qty": 15600.0,
        #                     "Unit": "KG",
        #                     "UnitPrice": 171.22,
        #                     "TotAmt": 2671032.0,
        #                     "Discount": 0.0,
        #                     # "PreTaxVal": 1,
        #                     "AssAmt": 2671032.0,
        #                     "GstRt": 5.0,
        #                     "IgstAmt": 133551.6,
        #                     # 2671032.0
        #                     "TotItemVal": 2804583.6
        #
        #                 }
        #             ],
        #             "ValDtls": {
        #                 "AssVal": 2671032.0,
        #                 "IgstVal": 133551.6,
        #                 "Discount": 0,
        #                 "TotInvVal": 2804583.6,
        #             },
        #             "ExpDtls": {
        #                 "ShipBNo": "6351151",
        #                 "ShipBDt": "01/04/2022"
        #             },
        #             "EwbDtls": {
        #                 "TransId": "12AWGPV7107B1Z1",
        #                 "TransName": "XYZ EXPORTS",
        #                 "Distance": 100,
        #                 "TransDocNo": "DOC01",
        #                 "TransDocDt": "10/08/2020",
        #                 "VehNo": "ka123456",
        #                 "VehType": "R",
        #                 "TransMode": "1"
        #             }
        #             },
        #         }
        #     }
        # ]
        # testeddate = self.documentdate
        # dt_obj = datetime.strptime(testeddate, '%Y-%m-%d %H:%M:%S')
        # formated = [
        #     {
        #         "transaction": {
        #             "Version": "1.1",
        #             "TranDtls": {
        #                 "TaxSch": "GST",
        #                 "SupTyp": "EXPWP",
        #                 "EcmGstin": None,
        #                 "IgstOnIntra": "N"
        #             },
        #             "DocDtls": {
        #                 "Typ": "INV",
        #                 "No": self.documentnumber,
        #                 "Dt": self.documentdate
        #             },
        #             "SellerDtls": {
        #                 "Gstin": "29AAFCD5862R000",
        #                 "LglNm": self.supplierlegalname,
        #                 "TrdNm": self.supplierlegalname,
        #                 "Addr1": self.supplieraddress1 or "",
        #                 "Loc": self.supplierplace or "",
        #                 "Pin": "562160",
        #                 "Stcd": "29",
        #             },
        #             "BuyerDtls": {
        #                 "Gstin": self.recipientgstin,
        #                 "LglNm": self.recipientlegalname,
        #                 "TrdNm": self.recipienttradename,
        #                 "Pos": self.placeofsupply or "",
        #                 "Addr1": self.recipientaddress1 or "",
        #                 "Loc": self.recipientplace or "",
        #                 "Pin": self.recipientpincode or "",
        #                 "Stcd": self.recipientstatecode or "",
        #             },
        #             "ShipDtls": {
        #                 "Gstin": "URP",
        #                 "LglNm": "India Gateway Terminal Private Limited",
        #                 "TrdNm": "India Gateway Terminal Private Limited",
        #                 "Addr1": "Administration Building, ICTT,",
        #                 "Addr2": "Vallarpadam SEZ, Mulavukadu Village",
        #                 "Loc": "Ernakulam",
        #                 "Pin": 562160,
        #                 "Stcd": 29
        #             },
        #             "ItemList": item_list,
        #             "ValDtls": {
        #                 "AssVal": AssVal,
        #                 "IgstVal": IgstVal,
        #                 "Discount": Discount,
        #                 "TotInvVal": TotInvVal,
        #             },
        #             "ExpDtls": {
        #                 "ShipBNo": self.shippingbillnumber or "",
        #                 "ShipBDt": self.shippingbilldate or "",
        #             }
        #         }
        #     }
        # ]

        # print(data,"data1c")
        # try:
        # req = requests.put(url, data=json.dumps(formated_original), headers=headers, timeout=50)
        # req.raise_for_status()
        # content = req.json()
        # print(content)
        # print(content[0]['govt_response']['Irn'])
        # if content[0]['govt_response']['Success'] == 'Y':
        #     self.irn = content[0]['govt_response']['Irn'] if content[0]['govt_response'][
        #                                                          'Success'] == 'Y' else False
        # else:
        #     self.irn = False
        # self.irn = content[0]['govt_response']['Irn'] if content[0]['govt_response']['Success'] == 'Y' else False
        # self.log = content[0]['document_status']
        # self.govt_log = content[0]['govt_response']

        # except IOError:
        #     error_msg = _("Required Fields Missing or Invalid Format For IRN generation.")
        #     raise self.env['res.config.settings'].get_config_warning(error_msg)

        # for row in cursor:
        #     print(row)

    # return self.env.ref('eastea-custom.purchase_order_report_qweb_paperform1').report_action(self)

#
