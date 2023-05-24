from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo import modules



class SaleLotNoUpload(models.TransientModel):
    _name = "salelotno.wizard"

    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS / XLSX File')],
                                     string='Select', default='xls')
    file_to_import = fields.Binary('Select File', help='Select File')
