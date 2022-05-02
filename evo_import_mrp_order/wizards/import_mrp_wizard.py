# -*- coding: utf-8 -*-

from odoo import fields, models, _
import base64
import xlrd
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.modules.module import get_resource_path

class ImportMrpWizard(models.TransientModel):
    _name = 'import.mrp.wizard'
    
    file = fields.Binary('File', help="File to check and/or import, raw binary (not base64)", attachment=False)
    file_name = fields.Char('File Name')
    
    
    def import_mrp_file(self):
        if not self.file:
            raise UserError(_('Please Upload file first.'))
        import_file = base64.b64decode(self.file)
        book = xlrd.open_workbook(file_contents=import_file or b'')
        sheets = book.sheet_names()
        data_length,sheet_data = self.env['base_import.import']._read_xls_book(book, sheets[0])
        
        mrp_bom_obj = self.env['mrp.bom']
        product_obj = self.env['product.product']
        mrp_production_obj = self.env['mrp.production']
        uom_obj = self.env['uom.uom']
        user_obj = self.env['res.users']
        
        count = 1
        mrp_list = []
        for row in sheet_data:
            if count == 1:
                count += 1
                continue
            
            if not row[0]:
                raise UserError(_('Product Code is empty in row %s' % count))
            if not row[1]:
                raise UserError(_('Product Unit of Measure is empty in row %s' % count))
            if not row[2]:
                raise UserError(_('Quantity is empty in row %s' % count))
            if not row[3]:
                raise UserError(_('Bill of Material Reference is empty in row %s' % count))
            if not row[4]:
                raise UserError(_('Scheduled Date is empty in row %s' % count))
            if not row[5]:
                raise UserError(_('Responsible is empty in row %s' % count))
            
            product_id = product_obj.sudo().search(['|', ('name', '=', row[0]),('default_code','=',row[0])],order='id desc', limit=1)
            if not product_id:
                raise UserError(_('For Product code: %s, Product: %s not found' % (row[0],row[0])))
            uom_id = uom_obj.sudo().search([('name','=',row[1])],limit=1)
            if not uom_id:
                raise UserError(_('In row: %s, Unit of Measure: %s not found' % (count,row[1])))
           
            bom_id = mrp_bom_obj.sudo().search(['|', ('product_tmpl_id.name','=',row[3]),('product_tmpl_id.default_code','=',row[3])],order='id desc',limit=1)
            if not bom_id:
                raise UserError(_('In row: %s, Bill of Material: %s not found' % (count,row[3])))
            user_id = user_obj.sudo().search([('name','=',row[5])],limit=1)
            if not user_id:
                raise UserError(_('In row: %s, User: %s not found' % (count,row[5])))
            
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            combine = row[4] + ' ' + str(current_time)
            mrp_list.append({'product_id': product_id.id,
                            'bom_id': bom_id.id,
                            'product_qty': float(row[2]),
                            'product_uom_id': uom_id.id if uom_id else product_id.uom_id.id,
                            'date_planned_start' : datetime.strptime(combine, DEFAULT_SERVER_DATETIME_FORMAT),
                            'user_id': user_id.id,
                            'company_id': user_id.company_id.id,
                            })
            
        for mrp in mrp_list:
            mrp_id = mrp_production_obj.sudo().create(mrp)
            mrp_id.sudo()._onchange_move_finished()
            mrp_id.sudo()._onchange_move_raw()
            mrp_id.sudo()._onchange_workorder_ids()
            mrp_id.sudo()._onchange_picking_type()
            mrp_id.sudo()._onchange_location()
            mrp_id.sudo()._onchange_location_dest()
        return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'All MRP records are imported',
                    'type': 'rainbow_man',
                    }
                }
    mrp_file_sample = fields.Binary('File Sample')
    
    def get_mrp_file_sample(self):
        path = get_resource_path('evo_import_mrp_order', 'data', 'MRP Order.xlsx')
        self.mrp_file_sample = base64.b64encode(open(path, 'rb').read()) if path else False
        return {
            'type': 'ir.actions.act_url',
            'name': 'contract',
            'url': '/web/content/import.mrp.wizard/%s/mrp_file_sample/MRP Order.xlsx?download=true' %(self.id),
     
        }
    