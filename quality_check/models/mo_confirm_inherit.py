from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger


class MoConfirmInherit(models.Model):
    _inherit = "mrp.production"

    # tags = fields.Selection([('pds', 'Pending'), ('pa', 'Passed'), ('fai', 'Failed')], string='Tags',compute='_compute_mo_tags', default='pds')

    tagss = fields.Selection([('pds', 'Pending'), ('pa', 'Passed'), ('fai', 'Failed')], string='Tags', default='pds')

    # categ = fields.Many2one(related='product_id.categ_id')

    #
    # def _compute_mo_tags(self):
    #     moqc = self.env['moqc.check'].search([('poid', '=', self.name)], limit=1) or False
    #
    #     if moqc:
    #         print(moqc.tag)
    #         moqc.tag = self.tags
    #
    #     else:
    #         self.tags = 'pds'




    def button_mark_done(self):
        # print("vurrok")

        # if self.state == "confirmed":

        qc = self.env['moqc.check'].search([('poid', '=', self.name)], limit=1) or False
        if not qc:
            raise ValidationError("Please Create the MOQC.")
        if qc:
            for l in qc:
                if l.state == "c":
                    self.state='confirmed'

                    super(MoConfirmInherit, self).button_mark_done()
                    if self.lot_producing_id:
                        l.lot_id = self.lot_producing_id

                        print(self.lot_producing_id)
                    # res = super(MoConfirmInherit, self).button_mark_done()

                    # Transfer creation
                    # if self.state == 'progress':

                    if l.failure ==True:
                        if self.lot_producing_id:

                            picking_type = request.env['stock.picking.type'].sudo().search(
                                [('name', 'like', 'Internal Transfers'),
                                 ('company_id', '=', self.company_id.id)], limit=1) or False

                            if picking_type:
                                so_loc=self.location_dest_id.id

                                source_loc = self.env['stock.location'].sudo().search(
                                    [('company_id', '=', self.company_id.id), ('id', '=', so_loc)])
                                if source_loc:
                                    print(source_loc.name)
                                    dest_loc = self.env['stock.location'].sudo().search(
                                        [('company_id', '=', self.company_id.id), ('name', 'like', "Damaged")])

                                    picking = request.env['stock.picking'].sudo().create({
                                        'location_id': source_loc.id,
                                        'location_dest_id': dest_loc.id,
                                        # 'partner_id': self.test_partner.id,
                                        'picking_type_id': picking_type.id,
                                        'immediate_transfer': False,
                                        'origin': self.name + " QC Failure",
                                        'company_id': self.company_id.id
                                    })

                                    move_receipt_1 = []

                                    move_receipt_1 = request.env['stock.move.line'].sudo().create({
                                        # 'name': self.name +" QC Failed",
                                        'product_id': self.product_id.id,
                                        'qty_done': self.qty_producing,
                                        # 'quantity_done': line["qty_done"],
                                        'product_uom_id': self.product_uom_id.id,
                                        'picking_id': picking.id,
                                        'picking_type_id': picking_type.id,
                                        'lot_id': self.lot_producing_id.id,
                                        'location_id': source_loc.id,
                                        'location_dest_id': dest_loc.id,
                                        'company_id': self.company_id.id
                                    })

                                else:
                                    raise ValidationError("Product Source Location Not Found")

                        # raise ValidationError("create trnsfer")

                    res = super(MoConfirmInherit, self).button_mark_done()
                    return res
                else:
                    if self.state == 'confirmed':
                        raise ValidationError("Please Verify the Quality Check.")


    def moqc_check(self):
        print("ppp")
        templates=[]

        if self.lot_producing_id:


            order = self.env['mrp.production'].search([('name', '=', self.name)], limit=1) or False

            temp = self.env['params.moqc'].search([('pdt_ctgrs', '=', self.product_id.categ_id.id )], limit=1) or False
            if temp:
                templates.append(temp.id)




            for line in order:

                vals = {
                    # 'tid': self.name,
                    'poid': self.name,
                    'name': self.name + " MOQC Check",
                    'qdate': self.date_planned_start,
                    'pdt_ctg_id': self.product_id.categ_id.id,
                    'product_id': self.product_id.id,
                    'pdt_temp_ids': templates,
                    'bld_sheet': self.blend,
                    'lot_id' : self.lot_producing_id.id,
                    'source_loc_id':self.location_src_id.id,
                    'dest_loc_id':self.location_dest_id.id,
                    # 'moqc_line_idss':moqc_line_idss
                }
                qua = self.env['moqc.check'].search([('poid', '=', self.name)], limit=1) or False
                if qua:

                    return {
                            }
                else:
                    new_package = self.env['moqc.check'].create(vals)
                    self.env.cr.commit()
                    new_pack = self.env['moqc.check'].search([('id', '=', new_package.id)], limit=1) or False
                    for rec in new_pack:
                        if rec.pdt_temp_ids:
                            lines = [(5, 0, 0)]
                            # lines = []
                            print("self.pdt_temp", new_package.pdt_temp_ids.moqc_params_line_ids)
                            for line in new_package.pdt_temp_ids.moqc_params_line_ids:
                                val = {
                                    'questionss': line.questions,

                                }
                                lines.append((0, 0, val))
                            rec.moqc_line_idss = lines

                    context = dict(self.env.context)
                    context['form_view_initial_mode'] = 'edit'
                    return {
                            }


        else:
            raise UserError("Please provide Lot number")

