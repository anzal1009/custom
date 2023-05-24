from odoo import api, models, fields, _
import xlrd
from odoo.exceptions import UserError
from odoo import modules
import logging

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')





class MOuploadCustom(models.TransientModel):
    _name = "mo.upload.wizard"

    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS / XLSX File')],
                                     string='Select', default='xls')
    file_to_import = fields.Binary('Select File', help='Select File')
    user = fields.Many2one('res.users',string='User')


    def prepare_excel_data(self, binary_data=False):
        if binary_data:
            xl_workbook = xlrd.open_workbook(file_contents=base64.decodebytes(binary_data))
            worksheet = xl_workbook.sheet_by_index(0)
            column_header = {}
            for col_index in range(worksheet.ncols):
                value = worksheet.cell(0, col_index).value.lower()
                column_header.update({col_index: value})
            data_list = []
            for row_index in range(1, worksheet.nrows):
                sheet_data = {}
                for col_index in range(worksheet.ncols):
                    sheet_data.update({
                        column_header.get(col_index): worksheet.cell(row_index, col_index).value or ''})
                if bool(sheet_data):
                    data_list.append(sheet_data)
            return data_list



    def import_file(self):
        if not self.file_to_import:
            raise UserError(_("Please select file First!"))
        if not self.user:
            raise UserError(_("Please select User!!"))

