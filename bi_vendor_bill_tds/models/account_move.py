# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning,ValidationError
import time
from odoo.tools import float_compare

class account_account(models.Model):
    _inherit = 'account.account'
    
    tds_account = fields.Boolean('TDS Account')
    
    
    
class account_move(models.Model):
    _inherit = 'account.move'



    def _compute_amount_after_tds(self):
        res = tds = 0.0
        for self_obj in self:
            if not self_obj.apply_tds:
                self_obj.tds_value = 0.0
            if self_obj.tds_value:    
                res = self_obj.amount_untaxed * (self_obj.tds_value/ 100)
            if self_obj.tds_amount and not self_obj.apply_tds:
                res = self_obj.tds_amount
            return res    



    @api.onchange('apply_tds')
    def onchange_apply_tds(self):
        if self.apply_tds:
            if self.move_type == 'in_invoice':
                account_search = self.env['account.account'].search([('tds_account', '=', True)])
                if account_search:
                    self.update({'tds_account':account_search[0].id})


    @api.depends(
    'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
    'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
    'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
    'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
    'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
    'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
    'line_ids.debit',
    'line_ids.credit',
    'line_ids.currency_id',
    'line_ids.amount_currency',
    'line_ids.amount_residual',
    'line_ids.amount_residual_currency',
    'line_ids.payment_id.state',
    'line_ids.full_reconcile_id',
    'tds_value',
    'amount_after_tds')
    def _compute_amount(self):
        for move in self:
  
            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue
  
            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()
  
            for line in move.line_ids:
                if line.currency_id and line in move._get_lines_onchange_currency():
                    currencies.add(line.currency_id)
  
                if move.is_invoice(include_receipts=True):
                    # === Invoices ===
  
                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                         
                        value = 0 
                        total_value = 0
                        if self._context.get('default_move_type') in ('in_invoice','in_receipt'):
                            for val in move.line_ids:
                                if not val.exclude_from_invoice_tab:
                                    total_value += val.debit
                                if val.tax_tag_ids:
                                    value+= val.debit
                                       
                            for rec in move.line_ids:        
                                if rec.tds_line == True or rec.name == 'Percent' :
                                    res = self._compute_amount_after_tds()
                                    tds_amt = res
                                    rec.credit = tds_amt
                                    rec.name = 'Percent'
                                    line.credit = total_value + value - rec.credit
                                    line.debit = 0.0
                                     
                         
                        elif self._context.get('default_move_type') == 'in_refund':
                            for val in move.line_ids:
                                if not val.exclude_from_invoice_tab:
                                   rec.total_value += val.credit
                                if val.tax_tag_ids:
                                    value+= val.credit
                                
                            for rec in move.line_ids:        
                                if rec.tds_line == True  or  rec.name == 'Percent':
                                    res = self._compute_amount_after_tds()
                                    tds_amt = res      
                                    rec.debit = tds_amt
                                    rec.name = 'Percent'
                                    line.debit = total_value + value - rec.debit            
                         
                         
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency
  
            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            res = self._compute_amount_after_tds()
            tds_amt = res
            move.tds_amount =  tds_amt
             
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total) - tds_amt
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total - tds_amt) if move.move_type == 'entry' else -total - tds_amt
            move.amount_residual_signed = total_residual - tds_amt
            move.amount_after_tds = move.amount_untaxed - tds_amt 
  
            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id
  
            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False
  
            if move.is_invoice(include_receipts=True) and move.state == 'posted':
  
                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'
  
            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search([('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])
  
                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped('line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'
  
            move.payment_state = new_pmt_state





                
                
         


    tds_value = fields.Float('TDS %',)
    tds_account = fields.Many2one('account.account', 'TDS Account')
    apply_tds = fields.Boolean('Apply TDS')
    amount_after_tds = fields.Monetary('Amount After TDS', store=True, readonly=True, tracking=True,compute='_compute_amount')
    tds_amount = fields.Monetary('-TDS Amount', store=True, readonly=True, tracking=True)
        
        
        
        
    @api.onchange('amount_untaxed','invoice_line_ids','tds_value','tds_account','line_ids')
    def _onchange_invoice_line_ids(self):
        current_invoice_lines = self.line_ids.filtered(lambda line: not line.exclude_from_invoice_tab)
        others_lines = self.line_ids - current_invoice_lines
        tds_lines = self.env['account.move.line']
    
        if self.apply_tds:
            count= 0
            for line in self.line_ids:
                if line.tds_line == True or line.name == 'Percent':
                    count+=1
                else:
                    pass 
            for line in self.line_ids:
                if count==1:
                    pass   
                else:
                    move_line_obj = line.search([('account_id','=',self.tds_account.id),('move_id', '=', self.id)],limit=1)
                    if not move_line_obj:   
                        res_x = self._compute_amount_after_tds()
                        tds_price = res_x
                           
                        if self._context.get('default_move_type') in ['in_invoice'] and tds_price != 0.0:
                            tds_vals = {
                                    'account_id' : self.tds_account.id,
                                    'price_unit' : -tds_price,
                                    'quantity': 1,
                                    'name': 'Percent',
                                    'exclude_from_invoice_tab': True,
                                    'tds_line': True,
                                    }
                             
                            tds_lines = self.line_ids.with_context(check_move_validity=False).new(tds_vals)
                         
                    else:
                        res_x = self._compute_amount_after_tds()
                        tds_price = res_x
                           
                        if move_line_obj:
                            price = -tds_price + move_line_obj.debit
                        else:
                            price = -tds_price
                        if self._context.get('default_move_type') in ['in_invoice']:
                            tds_lines = {
                                    'account_id' : self.tds_account.id,
                                    'price_unit' : price,
                                    'quantity': 1,
                                    'name': 'Percent',
                                    'exclude_from_invoice_tab': True,
                                    'tds_line': True,
                                    }
                        move_line_obj.with_context(check_move_validity=False).write(tds_lines) 
                                        
        if others_lines and current_invoice_lines - self.invoice_line_ids:
            others_lines[0].recompute_tax_line = True
        self.line_ids = others_lines + self.invoice_line_ids + tds_lines
        self._onchange_recompute_dynamic_lines()





    @api.model_create_multi
    def create(self, vals_list):
        res = super(account_move,self).create(vals_list)
        for val in vals_list:
            if res.apply_tds and (not res.tds_value):
                raise ValidationError(_('Please give the TDS values'))
            if res.apply_tds == True:
                sign = 1 if res.is_inbound() else -1
                name = []
                for line in res.line_ids:
                    name.append(line.name)
    
                                     
                if self._context.get('default_move_type') in ('in_invoice','in_receipt','out_refund'):
                    if self._context.get('default_purchase_id'):
                        for rec in self.line_ids:
                            if rec.tds_line == True:
                                value = self.amount_untaxed - self.amount_after_tds
                                account = self.tds_account.id
                                rec.with_context(check_move_validity=False).write({'price_unit':-value, 'name': 'Percent','account_id': account,})        
                            else:
                                pass
                    else:
                        if 'Percent' not in name:
                            res_x = res._compute_amount_after_tds()
                            tds_price = res_x         
                            tds_vals = {
                                'account_id' : res.tds_account.id,
                                'price_unit' : -tds_price,
                                'quantity': 1,
                                'name': 'Percent',
                                'exclude_from_invoice_tab': True,
                                'tds_line':True,
                                }
                            res.with_context(check_move_validity=False).write({
                                'line_ids' : [(0,0,tds_vals)]
                            }) 
                else:
                    pass                     
            else:
                pass    
        return res



    @api.onchange('tds_value')
    def onchange_type(self):
        if self._context.get('default_move_type') in ('in_invoice','in_receipt','out_refund'):
            for line in self.line_ids:
                name = line.name
                if name == False or name == '':
                    line.debit = 0.0      


    
    def write(self,vals):
        res = super(account_move, self).write(vals)
        for move in self:
            if move.apply_tds and not move.tds_value:
                raise ValidationError(_('Please give TDS values'))
        return res



class account_move_line(models.Model):
    _inherit = 'account.move.line' 
 
    tds_line = fields.Boolean('is tds line')                 



