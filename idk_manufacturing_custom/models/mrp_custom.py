# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


# class MrpProductionCustomCost(models.Model):
#     _inherit = "mrp.production"

#     def compute_mrp_cost(self):

#         stock_valuation = self.env['stock.valuation.layer'].sudo().search([('description', 'like', self.name)],
#                                                                           order='id ASC')
#         mrp_component_cost = 0
#         mrp_pdt_value = 0
#         for sv in stock_valuation:
#             if sv.stock_move_id.raw_material_production_id:
#                 sv.unit_cost = sv.stock_move_id.mrp_product_unit_cost
#                 sv.value = sv.stock_move_id.mrp_product_unit_cost * sv.quantity
#                 mrp_pdt_value = mrp_pdt_value + sv.value
#                 mrp_component_cost = mrp_component_cost + sv.stock_move_id.mrp_product_unit_cost
#                 component_name = sv.stock_move_id.product_id.name
#                 journal_ref = self.name + " - " + component_name
#                 #                 journal_ref = "KV/MO/00010 - Eastea 800 g Bottle-E(FG)"
#                 journal = self.env['account.move'].sudo().search([('ref', 'like', journal_ref)])
#                 if journal:
#                     journal.button_draft()
#                     journal.name = False
#                     journal.date = str(self.date_planned_start)
#                     for line in journal.line_ids:
#                         if float(line.amount_currency) > 0:
#                             line.name = journal_ref
#                             line.debit = float(sv.value) * -1
#                         elif float(line.amount_currency) < 0:
#                             line.name = journal_ref
#                             line.credit = float(sv.value) * -1
#                         elif float(line.amount_currency) == 0:
#                             if line.account_id.id == sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id:
#                                 line.name = journal_ref
#                                 line.credit = float(sv.value) * -1
#                             elif line.account_id.id == sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id:
#                                 line.name = journal_ref
#                                 line.debit = float(sv.value) * -1
# #                             debit_account = self.env['account.account'].sudo().search(
# #                                 [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id),
# #                                  ('company_id', '=', self.company_id.id)], limit=1) or False
# #                             credit_account = self.env['account.account'].sudo().search(
# #                                 [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id),
# #                                  ('company_id', '=', self.company_id.id)], limit=1) or False
# #                             journal_account = self.env['account.journal'].sudo().search(
# #                                 [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
# #                                 limit=1) or False
# #                             journal_entry = self.env['account.move'].sudo().create({
# #                                 'move_type': "entry",
# #                                 'ref': journal_ref,
# #                                 'date': str(self.date_planned_start),
# #                                 'journal_id': journal_account.id,
# #                                 'company_id': self.company_id.id,
# #                                 'line_ids': [(0, 0, {
# #                                     'name': journal_ref,
# #                                     'debit': int(sv.value * -1),
# #                                     'account_id': debit_account.id
# #                                 }), (0, 0, {
# #                                     'name': journal_ref,
# #                                     'credit': int(sv.value * -1),
# #                                     'account_id': credit_account.id
# #                                 })]

# #                             })
#                 else:
#                     debit_account = self.env['account.account'].sudo().search(
#                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id),
#                          ('company_id', '=', self.company_id.id)], limit=1) or False
#                     credit_account = self.env['account.account'].sudo().search(
#                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id),
#                          ('company_id', '=', self.company_id.id)], limit=1) or False
#                     journal_account = self.env['account.journal'].sudo().search(
#                         [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
#                         limit=1) or False
#                     journal_entry = self.env['account.move'].sudo().create({
#                         'move_type': "entry",
#                         'ref': journal_ref,
#                         'date': str(self.date_planned_start),
#                         'journal_id': journal_account.id,
#                         'company_id': self.company_id.id,
#                         'line_ids': [(0, 0, {
#                             'name': journal_ref,
#                             'debit': float(sv.value) * -1,
#                             'account_id': debit_account.id
#                         }), (0, 0, {
#                             'name': journal_ref,
#                             'credit': float(sv.value) * -1,
#                             'account_id': credit_account.id
#                         })]

#                     })
#             elif sv.stock_move_id.production_id:
#                 sv.unit_cost = mrp_pdt_value / sv.quantity
#                 sv.value = mrp_pdt_value * -1

#                 component_name = sv.stock_move_id.product_id.name
#                 journal_ref = self.name + " - " + component_name
#                 journal = self.env['account.move'].sudo().search([('ref', 'like', journal_ref)])
#                 if journal:
#                     journal.button_draft()
#                     journal.name = False
#                     journal.date = str(self.date_planned_start)
#                     for line in journal.line_ids:
#                         if float(line.amount_currency) > 0:
#                             line.name = journal_ref
#                             line.debit = float(sv.value)
#                         elif float(line.amount_currency) < 0:
#                             line.name = journal_ref
#                             line.credit = float(sv.value)
#                         elif float(line.amount_currency) == 0:
#                             if line.account_id.id == sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id:
#                                 line.name = journal_ref
#                                 line.credit = float(sv.value)
#                             elif line.account_id.id == sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id:
#                                 line.name = journal_ref
#                                 line.debit = float(sv.value)
# #                             debit_account = self.env['account.account'].sudo().search(
# #                                 [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id),
# #                                  ('company_id', '=', self.company_id.id)], limit=1) or False
# #                             credit_account = self.env['account.account'].sudo().search(
# #                                 [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id),
# #                                  ('company_id', '=', self.company_id.id)], limit=1) or False
# #                             journal_account = self.env['account.journal'].sudo().search(
# #                                 [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
# #                                 limit=1) or False
# #                             journal_entry = self.env['account.move'].sudo().create({
# #                                 'move_type': "entry",
# #                                 'ref': journal_ref,
# #                                 'date': str(self.date_planned_start),
# #                                 'journal_id': journal_account.id,
# #                                 'company_id': self.company_id.id,
# #                                 'line_ids': [(0, 0, {
# #                                     'name': journal_ref,
# #                                     'debit': int(mrp_pdt_value * -1),
# #                                     'account_id': credit_account.id
# #                                 }), (0, 0, {
# #                                     'name': journal_ref,
# #                                     'credit': int(mrp_pdt_value * -1),
# #                                     'account_id': debit_account.id
# #                                 })]
# #                             })
#                 else:
#                     debit_account = self.env['account.account'].sudo().search(
#                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id),
#                          ('company_id', '=', self.company_id.id)], limit=1) or False
#                     credit_account = self.env['account.account'].sudo().search(
#                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id),
#                          ('company_id', '=', self.company_id.id)], limit=1) or False
#                     journal_account = self.env['account.journal'].sudo().search(
#                         [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
#                         limit=1) or False
#                     journal_entry = self.env['account.move'].sudo().create({
#                         'move_type': "entry",
#                         'ref': journal_ref,
#                         'date': str(self.date_planned_start),
#                         'journal_id': journal_account.id,
#                         'company_id': self.company_id.id,
#                         'line_ids': [(0, 0, {
#                             'name': journal_ref,
#                             'debit': float(sv.value),
#                             'account_id': credit_account.id
#                         }), (0, 0, {
#                             'name': journal_ref,
#                             'credit': float(sv.value),
#                             'account_id': debit_account.id
#                         })]
#                     })
# # class MrpProductionCustomCost(models.Model):
# #     _inherit = "mrp.production"

# #     def compute_mrp_cost(self):

# #         stock_valuation = self.env['stock.valuation.layer'].sudo().search([('description', 'like', self.name)],
# #                                                                           order='id ASC')
# #         mrp_component_cost = 0
# #         mrp_pdt_value = 0
# #         for sv in stock_valuation:
# #             if sv.stock_move_id.raw_material_production_id:
# #                 sv.unit_cost = sv.stock_move_id.mrp_product_unit_cost
# #                 sv.value = sv.stock_move_id.mrp_product_unit_cost * sv.quantity
# #                 mrp_pdt_value = mrp_pdt_value + sv.value
# #                 mrp_component_cost = mrp_component_cost + sv.stock_move_id.mrp_product_unit_cost
# #                 component_name = sv.stock_move_id.product_id.name
# #                 journal_ref = self.name + " - " + component_name
# #                 #                 journal_ref = "KV/MO/00010 - Eastea 800 g Bottle-E(FG)"
# #                 journal = self.env['account.move'].sudo().search([('ref', '=', journal_ref)])
# #                 if journal:
# #                     journal.button_draft()
# #                     for line in journal.line_ids:
# #                         if float(line.amount_currency) > 0:
# #                             line.name = journal_ref
# #                             line.debit = sv.value * -1
# #                         elif float(line.amount_currency) < 0:
# #                             line.name = journal_ref
# #                             line.credit = sv.value * -1
# #                 else:
# #                     debit_account = self.env['account.account'].sudo().search(
# #                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id),
# #                          ('company_id', '=', self.company_id.id)], limit=1) or False
# #                     credit_account = self.env['account.account'].sudo().search(
# #                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id),
# #                          ('company_id', '=', self.company_id.id)], limit=1) or False
# #                     journal_account = self.env['account.journal'].sudo().search(
# #                         [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
# #                         limit=1) or False
# #                     journal_entry = self.env['account.move'].sudo().create({
# #                         'move_type': "entry",
# #                         'ref': journal_ref,
# #                         'date': self.date_planned_start,
# #                         'journal_id': journal_account.id,
# #                         'company_id': self.company_id.id,
# #                         'line_ids': [(0, 0, {
# #                             'name': journal_ref,
# #                             'debit': int(sv.value * -1),
# #                             'account_id': debit_account.id
# #                         }), (0, 0, {
# #                             'name': journal_ref,
# #                             'credit': int(sv.value * -1),
# #                             'account_id': credit_account.id
# #                         })]

# #                     })
# #             elif sv.stock_move_id.production_id:
# #                 sv.unit_cost = mrp_pdt_value / sv.quantity
# #                 sv.value = mrp_pdt_value * -1

# #                 component_name = sv.stock_move_id.product_id.name
# #                 journal_ref = self.name + " - " + component_name
# #                 journal = self.env['account.move'].sudo().search([('ref', '=', journal_ref)])
# #                 if journal:
# #                     journal.button_draft()
# #                     for line in journal.line_ids:
# #                         if float(line.amount_currency) > 0:
# #                             line.name = journal_ref
# #                             line.debit = sv.value
# #                         elif float(line.amount_currency) < 0:
# #                             line.name = journal_ref
# #                             line.credit = sv.value
# #                 else:
# #                     debit_account = self.env['account.account'].sudo().search(
# #                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id),
# #                          ('company_id', '=', self.company_id.id)], limit=1) or False
# #                     credit_account = self.env['account.account'].sudo().search(
# #                         [('id', '=', sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id),
# #                          ('company_id', '=', self.company_id.id)], limit=1) or False
# #                     journal_account = self.env['account.journal'].sudo().search(
# #                         [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
# #                         limit=1) or False
# #                     journal_entry = self.env['account.move'].sudo().create({
# #                         'move_type': "entry",
# #                         'ref': journal_ref,
# #                         'date': self.date_planned_start,
# #                         'journal_id': journal_account.id,
# #                         'company_id': self.company_id.id,
# #                         'line_ids': [(0, 0, {
# #                             'name': journal_ref,
# #                             'debit': int(sv.value),
# #                             'account_id': credit_account.id
# #                         }), (0, 0, {
# #                             'name': journal_ref,
# #                             'credit': int(sv.value),
# #                             'account_id': debit_account.id
# #                         })]
# #                     })
# # class MrpProductionCustomCost(models.Model):
# #     _inherit = "mrp.production"

# #     def compute_mrp_cost(self):

# #         stock_valuation = self.env['stock.valuation.layer'].sudo().search([('description', 'like', self.name)], order='id ASC')
# #         mrp_component_cost = 0
# #         mrp_pdt_value = 0
# #         for sv in stock_valuation:
# #             if sv.stock_move_id.raw_material_production_id:
# #                 sv.unit_cost = sv.stock_move_id.mrp_product_unit_cost
# #                 sv.value = sv.stock_move_id.mrp_product_unit_cost * sv.quantity
# #                 mrp_pdt_value = mrp_pdt_value + sv.value
# #                 mrp_component_cost = mrp_component_cost + sv.stock_move_id.mrp_product_unit_cost
# #                 component_name = sv.stock_move_id.product_id.name
# #                 journal_ref = self.name+" - "+component_name
# # #                 journal_ref = "KV/MO/00010 - Eastea 800 g Bottle-E(FG)"
# #                 journal = self.env['account.move'].sudo().search([('ref', 'like', journal_ref)])
# #                 journal.button_draft()
# #                 for line in journal.line_ids:                    
# #                     if float(line.amount_currency) > 0:
# #                         line.name = journal_ref
# #                         line.debit = sv.value*-1
# #                     elif float(line.amount_currency) < 0:
# #                         line.name = journal_ref
# #                         line.credit = sv.value*-1
# #             elif sv.stock_move_id.production_id:
# #                 sv.unit_cost = mrp_pdt_value / sv.quantity
# #                 sv.value = mrp_pdt_value * -1
                
# #                 component_name = sv.stock_move_id.product_id.name
# #                 journal_ref = self.name+" - "+component_name
# #                 journal = self.env['account.move'].sudo().search([('ref', 'like', journal_ref)])
# #                 journal.button_draft()
# #                 for line in journal.line_ids:                    
# #                     if float(line.amount_currency) > 0:
# #                         line.name = journal_ref
# #                         line.credit = sv.value
# #                     elif float(line.amount_currency) < 0:
# #                         line.name = journal_ref
# #                         line.debit = sv.value

class ConsolidatedSv:
    def __init__(self, product_id, unit_cost, value, account_mids, sv):
        self.product_id = product_id
        self.unit_cost = unit_cost
        self.value = value
        self.account_mids = [account_mids]
        self.sv = [sv]
        

class MrpProductionCustomCostLine(models.Model):
    _inherit = "stock.move"

    mrp_product_unit_cost = fields.Float(string="Product Unit Cost", default=0.0, digits=(16, 4),)

    
class MrpProductionCustomCost(models.Model):
    _inherit = "mrp.production"
    
    def compute_mrp_cost(self):
        stock_valuation = self.env['stock.valuation.layer'].sudo().search([('description', 'like', self.name)], limit=1)
        production_id=0
        if stock_valuation.stock_move_id.production_id.id:
            production_id=stock_valuation.stock_move_id.production_id.id
        else:
            production_id = stock_valuation.stock_move_id.raw_material_production_id.id
        raw_material = self.env['stock.move'].sudo().search(
            [('raw_material_production_id', '=', production_id)], order='id ASC')
        
        rm_ids=[]
        for rm in raw_material:
            rm_ids.append(rm.id)
            
        stock_valuation_ids = self.env['stock.valuation.layer'].sudo().search([('stock_move_id', 'in', rm_ids)])
        mrp_component_cost = 0
        mrp_pdt_value = 0
        account_move_ids=[]
        for sv in stock_valuation_ids:
            if sv.stock_move_id.raw_material_production_id:
                sv.unit_cost = sv.stock_move_id.mrp_product_unit_cost
                sv.value = sv.stock_move_id.mrp_product_unit_cost * sv.quantity
                mrp_pdt_value = mrp_pdt_value + sv.value
                mrp_component_cost = mrp_component_cost + sv.stock_move_id.mrp_product_unit_cost
                account_move_ids.append(sv.account_move_id.id)

        sv_consolidated = []
        sv_found = False
        for sv in stock_valuation_ids:
            sv_found = False
            for cons_sv in sv_consolidated:
                if cons_sv.product_id == sv.product_id:
                    cons_sv.unit_cost += sv.unit_cost
                    cons_sv.value += sv.value
                    cons_sv.account_mids.append(sv.account_move_id)
                    cons_sv.sv.append(sv)
                    sv_found = True
            if not sv_found:
                
                sv_consolidated.append(ConsolidatedSv(sv.product_id, sv.unit_cost, sv.value, sv.account_move_id, sv))
                
      
      
        journals = self.env['account.move'].sudo().search([('id', 'in', account_move_ids)])
        for journal in journals:
            journal.button_draft()
            journal.name = False
            journal.unlink()  
            
#             selected_sv=0
#             for sv in sv_consolidated:
#                 for sv_account_id in sv.account_mids:
#                     if sv_account_id.id==journal.id:
#                         selected_sv=sv;
            
#             component_name = selected_sv.product_id.name
#             journal_ref = self.name + " - " + component_name
#             for line in journal.line_ids:
#                 if float(line.amount_currency) > 0:
#                     line.name = journal_ref    
#                     line.debit = float(selected_sv.value) * -1
#                 elif float(line.amount_currency) < 0:
#                     line.name = journal_ref
#                     line.credit = float(selected_sv.value) * -1
#                 elif float(line.amount_currency) == 0:
#                     if line.account_id.id == selected_sv.product_id.categ_id.property_stock_account_output_categ_id.id:
#                         line.name = journal_ref
#                         line.credit = float(selected_sv.value) * -1
#                     elif line.account_id.id == selected_sv.product_id.categ_id.property_stock_valuation_account_id.id:
#                         line.name = journal_ref
#                         line.debit = float(selected_sv.value) * -1
     
    
        journal_account = self.env['account.journal'].sudo().search(
            [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
            limit=1) or False
        for sv in sv_consolidated:
                
            component_name = sv.product_id.name
            journal_ref = self.name + " - " + component_name
            
            journal_entry = self.env['account.move'].sudo().create({
                'move_type': "entry",
                'ref': journal_ref,
                'date': self.date_planned_start,
                'journal_id': journal_account.id,
                'company_id': self.company_id.id,
                'line_ids': [(0, 0, {
                    'name': journal_ref,
                    'debit': float(sv.value) * -1,
#                     'debit': 100,
                    'account_id': sv.product_id.categ_id.property_stock_valuation_account_id.id
#                     'account_id': 748
                }), (0, 0, {
                    'name': journal_ref,
                    'credit': float(sv.value) * -1,
#                     'credit': 100,
                    'account_id': sv.product_id.categ_id.property_stock_account_output_categ_id.id
#                     'account_id': 1099
                })]
            })
            for sv_move_ids in sv.sv:
              sv_move_ids.account_move_id = journal_entry.id
            
#             selected_sv=0
#             for sv in stock_valuation_ids:
#                 if sv.account_move_id.id==journal.id:
#                     selected_sv=sv;
#             component_name = selected_sv.stock_move_id.product_id.name
#             journal_ref = self.name + " - " + component_name
#             for line in journal.line_ids:
#                 if float(line.amount_currency) > 0:
#                     line.name = journal_ref    
#                     line.debit = float(selected_sv.value) * -1
#                 elif float(line.amount_currency) < 0:
#                     line.name = journal_ref
#                     line.credit = float(selected_sv.value) * -1
#                 elif float(line.amount_currency) == 0:
#                     if line.account_id.id == selected_sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id:
#                         line.name = journal_ref
#                         line.credit = float(selected_sv.value) * -1
#                     elif line.account_id.id == selected_sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id:
#                         line.name = journal_ref
#                         line.debit = float(selected_sv.value) * -1
            
          
                        
    ###Final_output product

        raw_material = self.env['stock.move'].sudo().search(
            [('production_id', '=', production_id)], order='id ASC')
        
        rm_ids=[]
        for rm in raw_material:
            rm_ids.append(rm.id)
            
        stock_valuation_ids = self.env['stock.valuation.layer'].sudo().search([('stock_move_id', 'in', rm_ids)])
        account_move_ids=[]
        for sv in stock_valuation_ids:
            if sv.stock_move_id.production_id:
                sv.unit_cost = (mrp_pdt_value / sv.quantity) * -1
                sv.value = mrp_pdt_value * -1
                account_move_ids.append(sv.account_move_id.id)

        stock_valuation_ids = self.env['stock.valuation.layer'].sudo().search([('stock_move_id', 'in', rm_ids)])
        
        journals = self.env['account.move'].sudo().search([('id', 'in', account_move_ids)])
        for journal in journals:
            journal.button_draft()
            journal.name = False
            journal.unlink() 
            
#             journal.date = str(self.date_planned_start)
            
#             selected_sv=0
#             for sv in stock_valuation_ids:
#                 if sv.account_move_id.id==journal.id:
#                     selected_sv=sv;
#             component_name = selected_sv.stock_move_id.product_id.name
#             journal_ref = self.name + " - " + component_name
# #             journal.line_ids[1].debit = 0
# #             journal.line_ids[0].credit = 0
# #             journal.line_ids[1].debit = 10
# #             journal.line_ids[0].credit = 10
#             for line in journal.line_ids:
#                 if float(line.amount_currency) > 0:
#                     line.name = journal_ref    
#                     line.debit = selected_sv.value
#                 elif float(line.amount_currency) < 0:
#                     line.name = journal_ref
#                     line.credit = selected_sv.value
#                 elif float(line.amount_currency) == 0:
#                     if line.account_id.id == selected_sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id:
# #                     if line.account_id.id == 748:
#                         line.name = journal_ref
#                         line.credit = selected_sv.value

#                     elif line.account_id.id == selected_sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id:
# #                     elif line.account_id.id == 1099:
#                         line.name = journal_ref
#                         line.debit = selected_sv.value

        journal_account = self.env['account.journal'].sudo().search(
            [('name', '=', "Inventory Valuation"), ('company_id', '=', self.company_id.id)],
            limit=1) or False
        for sv in stock_valuation_ids:
                
            component_name = sv.product_id.name
            journal_ref = self.name + " - " + component_name
            
            journal_entry = self.env['account.move'].sudo().create({
                'move_type': "entry",
                'ref': journal_ref,
                'date': self.date_planned_start,
                'journal_id': journal_account.id,
                'company_id': self.company_id.id,
                'line_ids': [(0, 0, {
                    'name': journal_ref,
                    'credit': float(sv.value),
#                     'debit': 100,
                    'account_id': sv.product_id.categ_id.property_stock_valuation_account_id.id
#                     'account_id': 748
                }), (0, 0, {
                    'name': journal_ref,
                    'debit': float(sv.value),
#                     'credit': 100,
                    'account_id': sv.product_id.categ_id.property_stock_account_output_categ_id.id
#                     'account_id': 1099
                })]
            })
            
            sv.account_move_id = journal_entry.id
#             for line in journal.line_ids:
              
#                 if float(line.amount_currency) > 0:
#                     line.name = journal_ref
#                     line.debit = 2926512.15                                     
#                 elif float(line.amount_currency) < 0:
#                     line.name = journal_ref
#                     line.credit = 2926512.15                    
#                 elif float(line.amount_currency) == 0:
# #                     if line.account_id.id == selected_sv.stock_move_id.product_id.categ_id.property_stock_account_output_categ_id.id:
#                     if line.account_id.id == 748:
#                         line.name = journal_ref
# #                         line.credit = float(selected_sv.value)
#                         line.credit = 2926512.15

# #                     elif line.account_id.id == selected_sv.stock_move_id.product_id.categ_id.property_stock_valuation_account_id.id:
#                     elif line.account_id.id == 1099:
#                         line.name = journal_ref
#                         line.debit = 2926512.15
