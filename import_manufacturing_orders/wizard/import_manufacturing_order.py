# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################
from odoo import models, fields, api, _
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


class ImportPickings(models.TransientModel):
    _name = "import.manufacturing.order"
    _description = "Import Manufacturing Orders"

    file_to_import = fields.Binary('Select File', help='Select File')
    import_product_by = fields.Selection([('name', 'Name'), ('code', 'Code'), ('barcode', 'Barcode')],
                                         string="Import Product By")
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS / XLSX File')],
                                     string='Select', default='xls')
    sequence_option = fields.Selection([('excel_csv', 'Use Excel/CSV Sequence Number'),
                                        ('system', 'Use System Default Sequence Number')],
                                       string="Sequence Option")
    datas = fields.Binary()

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

    def create_manufacturing_order(self, product, qty, deadline, company, responsible, import_product_by, uom,
                                   sequence_option, order):
        user_id = False
        product_id = False
        company_id = False
        bom_id = False
        product_uom = False
        move_raw_ids = False
        if uom:
            product_uom = self.env['uom.uom'].search([('name', '=', uom)])
        if not product_uom:
            raise Warning(_("Unit OF Measurement Not Found {} !!").format(uom))
        if company:
            company_id = self.env['res.company'].search([('name', '=', company)])
        if not company_id:
            raise Warning(_("Company not Found!!"))
        if import_product_by == 'code':
            product_id = self.env['product.product'].search([('default_code', '=', product)])
        if import_product_by == 'name':
            product_id = self.env['product.product'].search([('name', '=', product)])
        if import_product_by == 'barcode':
            product_id = self.env['product.product'].search([('barcode', '=', product)])
        if not product_id:
            raise Warning(_("Product Not Found {} !!").format(product))
        if responsible:
            user_id = self.env['res.users'].search([('name', '=', responsible)])
        if not user_id:
            raise Warning(_("Responsible Person Not Found {} !!").format(product))
        if product_id and product_id.product_tmpl_id:
            bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', product_id.product_tmpl_id.id)],limit=1)
        if not bom_id:
            raise Warning(_("Bill Of Material Not Found {} !!").format(product))
        vals = {
            'product_id': product_id.id,
            'bom_id': bom_id.id,
            'user_id': user_id.id,
            'company_id': company_id.id,
            'date_planned_start': deadline,
            'product_qty': float(qty),
            'product_uom_id': product_uom.id

        }
        if sequence_option == 'excel_csv':
            vals.update({
                'name': order
            })
        mo = self.env['mrp.production'].create(vals)
        mo._onchange_move_raw()
        for rec in mo.move_raw_ids:
            mo.action_confirm() 
        return mo

    def download_sample_file(self):
        file_name = False
        if not self.import_option:
            raise UserError(_("Please select one options"))
        if self.import_option == 'csv':
            file_name = 'manufacturing_orders_product_code.csv'
        if self.import_option == 'xls':
            file_name = 'manufacturing_orders_code.xls'
        if file_name:
            with open(modules.get_module_resource('import_manufacturing_orders', 'Sample/', file_name),
                      'rb') as f:
                file = base64.b64encode(f.read())
            self.write({'datas': file})
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/?download=1&model=import.manufacturing.order&field=datas&id=%s&filename=%s' % (
                    self.id, file_name),
                'target': 'self',
            }

    def import_file(self):
        if not self.file_to_import:
            raise UserError(_("Please select file First!"))
        if not self.import_product_by:
            raise UserError(_("Please select product Option!!"))
        if not self.sequence_option:
            raise UserError(_("Please select Sequence Option!!"))
        mo_ids = []
        mo_available_list = []

        if self.import_option == 'csv':
            try:
                data = base64.b64decode(self.file_to_import).decode('utf-8')
                lines = data.splitlines()
                reader = csv.DictReader(lines, delimiter=',')
            except:
                raise UserError(_("Invalid file!"))
            for line in reader:
                product = False
                product = line.get('product name', False)
                if not product:
                    product = line.get('product code', False)
                if not product:
                    product = line.get('product barcode', False)
                qty = line.get('qty', False)
                deadline = line.get('deadline', False)
                company = line.get('company', False)
                responsible = line.get('responsible', False)
                uom = line.get('uom', False),
                order = line.get('name', False)
                if not product or not qty:
                    raise UserError(_("Please check file data!!"))
                if self.import_product_by == 'code':
                    product_id = self.env['product.product'].search([('default_code', '=', product)], limit=1)
                if self.import_product_by == 'name':
                    product_id = self.env['product.product'].search([('name', '=', product)], limit=1)
                if self.import_product_by == 'barcode':
                    product_id = self.env['product.product'].search([('barcode', '=', product)], limit=1)
                if not product_id:
                    raise UserError(_("Product Not Found {} !!").format(product))
                if product_id:
                    mo = self.env['mrp.production'].search(
                        [('product_id', '=', product_id.id), ('state', '=', 'cancel')], order="id desc", limit=1)
                    if mo:
                        mo_available_list.append(mo.id)
                    if not mo:
                        mo = self.create_manufacturing_order(product, qty, deadline, company, responsible,
                                                             self.import_product_by, uom, self.sequence_option, order)
                        if mo:
                            mo_ids.append(mo.id)
        if self.import_option == 'xls' and self.file_to_import:
            try:
                data_list = self.prepare_excel_data(self.file_to_import)
            except:
                raise UserError(_("Invalid file!"))
            for line in data_list:
                product = False
                product = line.get('product name', False)
                if not product:
                    product = line.get('product code', False)
                if not product:
                    product = line.get('product barcode', False)
                qty = line.get('qty', False)
                deadline = line.get('deadline', False)
                company = line.get('company', False)
                responsible = line.get('responsible', False)
                uom = line.get('uom', False)
                order = line.get('name', False)
                if not product or not qty:
                    raise UserError(_("Please check file data!!"))
                if self.import_product_by == 'code':
                    product_id = self.env['product.product'].search([('default_code', '=', product)], limit=1)
                if self.import_product_by == 'name':
                    product_id = self.env['product.product'].search([('name', '=', product)], limit=1)
                if self.import_product_by == 'barcode':
                    product_id = self.env['product.product'].search([('barcode', '=', product)], limit=1)
                if not product_id:
                    raise UserError(_("Product Not Found {} !!").format(product))
                if product_id:
                    mo = self.env['mrp.production'].search(
                        [('product_id', '=', product_id.id), ('state', '=', 'cancel')], order="id desc", limit=1)
                    if mo:
                        mo_available_list.append(mo.id)
                    if not mo:
                        mo = self.create_manufacturing_order(product, qty, deadline, company, responsible,
                                                             self.import_product_by, uom, self.sequence_option, order)
                        if mo:
                            mo_ids.append(mo.id)

        if mo_ids:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "Manufacturing Orders Successfully Imported",
                    'img_url': '/import_manufacturing_orders/static/src/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
        if mo_available_list:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "Manufacturing Orders Already Imported",
                    'img_url': '/import_manufacturing_orders/static/src/img/smile.svg',
                    'type': 'rainbow_man',
                }
            }
