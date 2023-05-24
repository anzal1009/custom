from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger


class QualityTransfer(models.Model):
    _inherit = 'stock.picking'

    tagss = fields.Selection([('pds', 'Pending'), ('pa', 'Passed'), ('fai', 'Failed')], string='Tags', default='pds')

    def button_validate(self):
        qc_prdt_line_ids = []

        for stk in self:
            print(stk.picking_type_id)
            for stk_line in stk.move_ids_without_package:
                print(stk_line.product_id.categ_id)

                dest_lo = self.env['stock.location'].sudo().search(
                    [('company_id', '=', self.company_id.id), ('name', '=', "Quality Damaged")])

                if dest_lo.id == self.location_dest_id.id:
                    res = super(QualityTransfer, self).button_validate()
                    return res

                else:

                    params = self.env['quality.params'].search([('pdt_ctgs', '=', stk_line.product_id.categ_id.id),
                                                                ('operation_type', '=', stk.picking_type_id.id)],
                                                               limit=1) or False
                    # print(params.id)
                    if params:
                        # if self.picking_type_id.name == "Receipts":
                        trnsfer = self.env['stock.picking'].search([('name', '=', self.name)], limit=1) or False
                        # if trnsfer:
                        # trnsfer.quality_check()
                        qc = self.env['custom.quality.check'].search([('tid', '=', self.name)], limit=1) or False
                        if qc:
                            for l in qc:
                                if l.state == "c":
                                    res = super(QualityTransfer, self).button_validate()
                                    #                                     super(QualityTransfer, self).button_validate()
                                    # return res
                                    l.state_hide = True
                                    for lots in l.qc_prdt_line_ids:
                                        lot_name = lots.p_line_lot
                                        pdt_names = lots.product_id_line

                                        # print("CONNNECTEDDDDDDDDDDDDDDD")

                                        lot_id = self.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', self.company_id.id), ('name', '=', lot_name),
                                             ('product_id', '=', pdt_names.id)])
                                        if lot_id:
                                            lots.p_line_lot_id = lot_id.id

                                    #                                         res = super(QualityTransfer, self).button_validate()

                                    # #################### Creating Back Transfer #####################

                                    for qc_lines in l.qc_prdt_line_ids:
                                        if qc_lines.p_responce == 'F':
                                            # print(qc_lines.product_id_line.id)
                                            # print(qc_lines.p_line_lot_id.id)

                                            pdt_catgs = qc_lines.product_id_line.categ_id.name
                                            # print(pdt_catgs)

                                            if pdt_catgs:

                                                picking_type = request.env['stock.picking.type'].sudo().search(
                                                    [('name', 'like', 'Internal Transfers'),
                                                     ('company_id', '=', self.company_id.id)], limit=1) or False

                                                if picking_type:

                                                    #                                                     source_loc = self.env['stock.location'].sudo().search(
                                                    #                                                             [('company_id', '=', self.company_id.id), ('name', 'like',pdt_catgs)])
                                                    #                                                     print(pdt_catgs)
                                                    #                                                     print(source_loc)
                                                    #                                                     if source_loc:

                                                    dest_loc = self.env['stock.location'].sudo().search(
                                                        [('company_id', '=', self.company_id.id),
                                                         ('name', 'like', "Quality Damaged")])
                                                    if dest_loc:

                                                        picking = request.env['stock.picking'].sudo().create({
                                                            'location_id': self.location_dest_id.id,
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
                                                            'product_id': qc_lines.product_id_line.id,
                                                            'qty_done': qc_lines.p_qty,
                                                            # 'quantity_done': line["qty_done"],
                                                            'product_uom_id': qc_lines.product_id_line.uom_id.id,
                                                            'picking_id': picking.id,
                                                            'picking_type_id': picking_type.id,
                                                            'lot_id': qc_lines.p_line_lot_id.id,
                                                            'location_id': self.location_dest_id.id,
                                                            'location_dest_id': dest_loc.id,
                                                            'company_id': self.company_id.id
                                                        })

                                                        if picking:
                                                            picking.action_confirm()
                                                            #                                                             picking.action_assign()
                                                            #                                                             picking.action_set_quantities_to_reservation()
                                                            picking.button_validate()
                                                        return res


                                                    else:
                                                        raise ValidationError("Destination Location Not Found")

                                                else:
                                                    raise ValidationError("Operation Not Found")

                                                # print(source_loc.name)
                                                # print(dest_loc.name)
                                                # print(picking_type.name)
                                            else:
                                                raise ValidationError("Product Category not Found.")

                                            # raise ValidationError("Please Verify")

                                #                                     return res

                                # raise UserError(
                                #     _("Transfer Created %s.") % picking.name)
                                #
                                # return res

                                else:
                                    raise ValidationError("Please Verify the Quality Check.")


                        else:
                            raise ValidationError("Please Verify the done quantity or quality check.")


                    else:
                        res = super(QualityTransfer, self).button_validate()
                        return res

    def quality_check(self):
        params = self.env['quality.params'].search(
            [('pdt_ctgs', '=', self.move_ids_without_package.product_id.categ_id.id),
             ('operation_type', '=', self.picking_type_id.id)], limit=1) or False
        # print(params.id)
        if params:

            # print(self.origin)
            # tid = self.env['quality.check'].sudo().search(
            #     [('tid', '=', self.name)])
            # if tid:
            #     raise ValidationError("Quality already Initiated.")

            # if self.origin:

            order = self.env['stock.picking'].search([('name', '=', self.name)], limit=1) or False
            products = []
            catg = []
            templates = []
            qc_prdt_line_ids = []
            lots = []
            lot_no = []
            # lot_id=[]

            print(self.picking_type_id.name)

            for line in order:
                for l in line.move_ids_without_package:

                    if l.move_line_nosuggest_ids:
                        # print("yess")

                        #### For Product Creation

                        pdt_id = l.product_id.id
                        product_id = self.env['product.product'].search([('id', '=', pdt_id)], limit=1) or False
                        # print(product_id.id)

                        #### For Lot no

                        for lines in l.move_line_nosuggest_ids:
                            if lines.lot_name:

                                qc_prdt_line_ids.append((0, 0, {
                                    'product_id_line': product_id.id,
                                    'p_qty': lines.qty_done,
                                    'p_line_lot': lines.lot_name
                                }))

                            elif lines.lot_id:
                                qc_prdt_line_ids.append((0, 0, {
                                    'product_id_line': product_id.id,
                                    'p_qty': lines.qty_done,
                                    'p_line_lot': lines.lot_id.name
                                }))


                            else:
                                qc_prdt_line_ids.append((0, 0, {

                                    'product_id_line': product_id.id,
                                    'p_qty': l.quantity_done,

                                }))


                    else:
                        raise ValidationError("Please Confirm Done Quantities")

                    #### For Product Category

                    product_catgry = l.product_id.categ_id

                    prodt_ctg = self.env['product.category'].search([('name', '=', product_catgry.name)],
                                                                    limit=1) or False

                    catg.append(prodt_ctg.id)
                    # print(catg)

                    #### Template updation

                    if prodt_ctg:
                        # print(self.name)

                        template = self.env['quality.params'].search([('pdt_ctgs', '=', prodt_ctg.id),
                                                                      ('operation_type', '=', self.picking_type_id.id)],
                                                                     limit=1) or False
                        # print(template.name)
                        if template:
                            templates.append(template.id)
                            # print(template.id)

                vals = {
                    'tid': self.name,
                    'poid': self.origin,
                    'pdt_ctg_ids': catg,
                    'name': self.name + "  QC Check",
                    'qdate': self.scheduled_date,
                    'pdt_temp_ids': templates,
                    'qc_prdt_line_ids': qc_prdt_line_ids,
                    'op_type': self.picking_type_id.id
                    # 'lot': self.lot_producing_id.name
                }

                qua = self.env['custom.quality.check'].search([('tid', '=', self.name)], limit=1) or False
                if qua:
                    # raise ValidationError("Plz Check QC.")
                    return {

                    }
                else:
                    new_package = self.env['custom.quality.check'].create(vals)
                    self.env.cr.commit()
                    new_pack = self.env['custom.quality.check'].search([('id', '=', new_package.id)], limit=1) or False

                    for rec in new_pack:
                        # print("sdyfygsidu")
                        if rec.pdt_temp_ids:
                            lines = [(5, 0, 0)]
                            # lines = []
                            # print("self.pdt_temp", self.pdt_temp.qc_params_line_ids)
                            for line in new_package.pdt_temp_ids.qc_params_line_ids:
                                val = {
                                    'questionss': line.questions,

                                }
                                if line.questions:
                                    lines.append((0, 0, val))
                            rec.qc_line_idss = lines

                    context = dict(self.env.context)
                    context['form_view_initial_mode'] = 'edit'
                    return {
                    }





# #################################################################




from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import modules
from odoo.http import request, _logger


class QualityTransfer(models.Model):
    _inherit = 'stock.picking'

    tagss = fields.Selection([('pds', 'Pending'), ('pa', 'Passed'), ('fai', 'Failed')], string='Tags', default='pds')

    def button_validate(self):
        qc_prdt_line_ids = []

        for stk in self:
            print(stk.picking_type_id)
            for stk_line in stk.move_ids_without_package:
                print(stk_line.product_id.categ_id)

                if stk_line.quantity_done == 0:

                    raise ValidationError("Pls confirm Done Quantities")

                else:

                    dest_lo = self.env['stock.location'].sudo().search(
                            [('company_id', '=', self.company_id.id), ('name', 'like',"Damaged")])

                    if dest_lo.id == self.location_dest_id.id:
                        res = super(QualityTransfer, self).button_validate()
                        return res

                    else:


                        params = self.env['quality.params'].search([('pdt_ctgs','=', stk_line.product_id.categ_id.id),
                                                                    ('operation_type','=',stk.picking_type_id.id)], limit=1) or False
                        # print(params.id)
                        if params:
                        # if self.picking_type_id.name == "Receipts":
                            trnsfer = self.env['stock.picking'].search([('name','=', self.name)], limit=1) or False
                            # if trnsfer:
                                # trnsfer.quality_check()
                            qc = self.env['custom.quality.check'].search([('tid','=',self.name)], limit=1) or False
                            if qc:
                                for l in qc:
                                    if l.state == "c":

                                        res = super(QualityTransfer, self).button_validate()
                                        # return res



                                        # stk_line.quantity_done = stk_line.reserved_availability


                                        # res =  super(QualityTransfer, self).button_validate()
                                        # return res

                                        l.state_hide = True
                                        for lots in l.qc_prdt_line_ids:
                                            lot_name = lots.p_line_lot
                                            pdt_names = lots.product_id_line

                                            print("CONNNECTEDDDDDDDDDDDDDDD")

                                            lot_id = self.env['stock.production.lot'].sudo().search(
                                                            [('company_id', '=', self.company_id.id), ('name', '=',lot_name),
                                                             ('product_id', '=',pdt_names.id)])
                                            if lot_id:
                                                lots.p_line_lot_id = lot_id.id
                                            # return res

                                        # super(QualityTransfer, self).button_validate()
                                        # return res

                # #################### Creating Back Transfer #####################

                                        # return res

                                        for qc_lines in l.qc_prdt_line_ids:
                                            if qc_lines.p_responce == 'F':
                                                # print(qc_lines.product_id_line.id)
                                                # print(qc_lines.p_line_lot_id.id)

                                                pdt_catgs = qc_lines.product_id_line.categ_id.name
                                                # print(pdt_catgs)

                                                if pdt_catgs:

                                                    picking_type = request.env['stock.picking.type'].sudo().search(
                                                        [('name', 'like', 'Internal Transfers'),
                                                         ('company_id', '=', self.company_id.id)], limit=1) or False

                                                    if picking_type:

                                                        dest_loc = self.env['stock.location'].sudo().search(
                                                                [('company_id', '=', self.company_id.id), ('name', 'like',"Damaged")])

                                                        if dest_loc:

                                                            picking = request.env['stock.picking'].sudo().create({
                                                                'location_id': self.location_dest_id.id,
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
                                                                'product_id': qc_lines.product_id_line.id,
                                                                'qty_done':qc_lines.p_qty,
                                                                # 'product_uom_qty':qc_lines.p_qty,
                                                                # 'quantity_done': line["qty_done"],
                                                                'product_uom_id': qc_lines.product_id_line.uom_id.id,
                                                                'picking_id': picking.id,
                                                                'picking_type_id': picking_type.id,
                                                                'lot_id':qc_lines.p_line_lot_id.id,
                                                                'location_id': self.location_dest_id.id,
                                                                'location_dest_id': dest_loc.id,
                                                                'company_id': self.company_id.id
                                                            })

                                                            if picking:
                                                                picking.action_confirm()
                                                                # picking.action_assign()
                                                                # picking.action_set_quantities_to_reservation()
                                                                picking.button_validate()

                                                            # res=super(QualityTransfer, self).button_validate()
                                                                return res

                                                        else:
                                                            raise ValidationError("Product Destination Location Not Found")

                                                    else:
                                                        raise ValidationError("Operation Not Found")


                                                    # print(source_loc.name)
                                                    # print(dest_loc.name)
                                                    # print(picking_type.name)
                                                else:
                                                    raise ValidationError("Product Category not Found.")

                                                # raise ValidationError("Please Verify")

                                        # return res

                                        # raise UserError(
                                        #     _("Transfer Created %s.") % picking.name)
                                        #
                                        # return res


                                    else:
                                        raise ValidationError("Please Verify the Quality Check.")


                            else:
                                raise ValidationError("Please Verify the done quantity or quality check.")


                        else:
                            res = super(QualityTransfer, self).button_validate()
                            return res
                # else:
                #     res = super(QualityTransfer, self).button_validate()
                #     return res




    def quality_check(self):

        params = self.env['quality.params'].search([('pdt_ctgs', '=', self.move_ids_without_package.product_id.categ_id.id),
                                                    ('operation_type', '=', self.picking_type_id.id)], limit=1) or False
        # print(params.id)
        if params:


            # print(self.origin)
            # tid = self.env['quality.check'].sudo().search(
            #     [('tid', '=', self.name)])
            # if tid:
            #     raise ValidationError("Quality already Initiated.")

            # if self.origin:

            order = self.env['stock.picking'].search([('name', '=', self.name)], limit=1) or False
            products =[]
            catg = []
            templates=[]
            qc_prdt_line_ids = []
            lots =[]
            lot_no=[]
            # lot_id=[]

            print(self.picking_type_id.name)

            for line in order:
                for l in line.move_ids_without_package:

                    if l.move_line_nosuggest_ids:
                        # print("yess")

                        #### For Product Creation

                        pdt_id = l.product_id.id
                        product_id = self.env['product.product'].search([('id', '=', pdt_id)], limit=1) or False
                        # print(product_id.id)

                        #### For Lot no

                        for lines in l.move_line_nosuggest_ids:
                            if lines.lot_name:


                                qc_prdt_line_ids.append((0, 0, {
                                    'product_id_line': product_id.id,
                                    'p_qty': lines.qty_done,
                                    'p_line_lot': lines.lot_name
                                }))

                            elif lines.lot_id:
                                qc_prdt_line_ids.append((0, 0, {
                                    'product_id_line': product_id.id,
                                    'p_qty': lines.qty_done,
                                    'p_line_lot': lines.lot_id.name
                                }))


                            else:
                                qc_prdt_line_ids.append((0, 0, {

                                     'product_id_line': product_id.id,
                                     'p_qty': l.quantity_done,

                                }))


                    else:
                        raise ValidationError("Please Confirm Done Quantities")




                    #### For Product Category

                    product_catgry = l.product_id.categ_id

                    prodt_ctg = self.env['product.category'].search([('name', '=', product_catgry.name)], limit=1) or False

                    catg.append(prodt_ctg.id)
                    # print(catg)


                    #### Template updation

                    if prodt_ctg:
                        # print(self.name)

                        template = self.env['quality.params'].search([('pdt_ctgs', '=',prodt_ctg.id ),
                                          ('operation_type','=',self.picking_type_id.id)], limit=1) or False
                        # print(template.name)
                        if template:
                            templates.append(template.id)
                            # print(template.id)


                vals = {
                    'tid': self.name,
                    'poid': self.origin,
                    'pdt_ctg_ids': catg,
                    'name' : self.name + "  QC Check",
                    'qdate': self.scheduled_date,
                    'pdt_temp_ids':templates,
                    'qc_prdt_line_ids':qc_prdt_line_ids,
                    'op_type':self.picking_type_id.id
                    # 'lot': self.lot_producing_id.name
                }




                qua = self.env['custom.quality.check'].search([('tid', '=', self.name)], limit=1) or False
                if qua:
                    # raise ValidationError("Plz Check QC.")
                    return {

                            }
                else:
                    new_package = self.env['custom.quality.check'].create(vals)
                    self.env.cr.commit()
                    new_pack = self.env['custom.quality.check'].search([('id', '=', new_package.id)], limit=1) or False

                    for rec in new_pack:
                        # print("sdyfygsidu")
                        if rec.pdt_temp_ids:
                            lines = [(5, 0, 0)]
                            # lines = []
                            # print("self.pdt_temp", self.pdt_temp.qc_params_line_ids)
                            for line in new_package.pdt_temp_ids.qc_params_line_ids:
                                val = {
                                    'questionss': line.questions,

                                }
                                if line.questions:
                                    lines.append((0, 0, val))
                            rec.qc_line_idss = lines

                    context = dict(self.env.context)
                    context['form_view_initial_mode'] = 'edit'
                    return {
                            }



