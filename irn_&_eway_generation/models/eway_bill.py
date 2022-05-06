import json



from odoo import  models, fields
import requests




class IrnInherit(models.Model):
    _inherit = "account.move"

    EwbNo = fields.Char(string="EWB No")
    EwbDt = fields.Date(string="EWB Date")
    EwbValidTill = fields.Date(string="EWB Valid Till")
    log = fields.Char(string="Log")
    TransName = fields.Char(string="Transport Name")
    TransDocNo = fields.Char(string="Transport DocNo")
    TransDocDt = fields.Date(string="Transport Doc Date *")
    TransId = fields.Char(string="Transport Id")
    VehNo = fields.Char(string="Vehicle No")
    VehType = fields.Char(string="Vehicle Type")
    TransMode = fields.Char(string="Transport Mode")
    dist = fields.Char(string="Distance")
    eway = fields.Char(string="E log")
    done = fields.Char(string="E WAY status")
    govt_log = fields.Char(string="Government Log")

    Stcd=fields.Char(string="State Code")
    Loc=fields.Char(string="Location")
    disloc=fields.Char(string="Dispatch Location")
    disstc=fields.Char(string="Dispatch StateCode")




class EwayBillInherit(models.Model):
    _inherit = 'account.move'


    def action_generate_e_way(self):
        if not self.Irn:
            raise self.env['res.config.settings'].get_config_warning("Generate IRN First")

        # Clear Tax Sandbox Credentials for Testing
        company_owner_id = "ba215e2e-bb17-4350-adcc-11b88d04278a"
        company_auth_token = "1.4b3bb028-184a-4608-baca-c1614d9b98f0_a2ec4a95e373e12cd7f8f54473f476aea038082134f19e8bc03f69080f288148"
        company_gstin = "32AACCE3723D1ZB"

        url = "https://einvoicing.internal.cleartax.co/v2/eInvoice/ewaybill"
        #         url = "https://api-einv.cleartax.in/v2/eInvoice/generate"
        headers = {"Content-type": "application/json",
                   "x-cleartax-auth-token": company_auth_token,
                   "x-cleartax-product": "EInvoice", "owner_id": company_owner_id,
                   "gstin": company_gstin}

        data = [
            {
                "Irn": self.Irn,
                "Distance": self.dist,
                "TransMode": self.TransMode,
                "TransId": self.partner_id.vat,
                "TransName": self.TransName,
                "TransDocDt": self.TransDocDt,
                "TransDocNo": self.TransDocNo,
                "VehNo": self.VehNo,
                "VehType": self.VehType,
                "ExpShipDtls": {
                    "Addr1": self.partner_id.street,
                    "Addr2": self.partner_id.street2,
                    "Loc": self.Loc ,
                    "Pin": self.partner_id.zip,
                    "Stcd": self.Stcd
                },
                "DispDtls": {
                    "Nm": self.company_id.name,
                    "Addr1":self.company_id.street,
                    "Addr2": self.company_id.street2,
                    "Loc": self.disloc,
                    "Pin": self.company_id.zip,
                    "Stcd": self.disstc
                }
            }]

        # try:
        req = requests.post(url, data=json.dumps(data), headers=headers, timeout=50)
        req.raise_for_status()
        content = req.json()
        print(content[0]['govt_response'])

        if content[0]['govt_response']['Success'] == 'Y':
            self.done = content[0]['govt_response']['Success'] if content[0]['govt_response'][
                                                                      'Success'] == 'Y' else False
            self.eway = content[0]['ewb_status']
        #     # self.AckNo = content[0]['govt_response']['AckNo']
        #     # self.AckDt = content[0]['govt_response']['AckDt']
            self.EwbNo = content[0]['govt_response']['EwbNo']
            self.EwbDt = content[0]['govt_response']['EwbDt']
            self.EwbValidTill = content[0]['govt_response']['EwbValidTill']
        #     self.Success = content[0]['govt_response']['Success']
        #     # self.SignedInvoice = content[0]['govt_response']['SignedInvoice']
        #
        else:
            self.EwbNo = False
            self.govt_log = content[0]['govt_response']['ErrorDetails']
        self.log = content[0]['ewb_status']