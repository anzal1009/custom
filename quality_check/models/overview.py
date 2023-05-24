from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo import modules
from odoo.http import request, _logger


class QualityOverview(models.Model):
    _name = 'quality.overview'

    name = fields.Char("Name")
    id_name = fields.Char("Id")

    draft_count = fields.Integer(string="Draft Count",compute ="_compute_draft_count" )
    pending_count = fields.Integer(string="Pending Count",compute ="_compute_pending_count" )
    completed_count = fields.Integer(string="Completed Count",compute ="_compute_completed_count" )


    def _compute_draft_count(self):
        for rec in self:
            if rec.name == "GRN QC":
                draft =self.env['custom.quality.check'].search_count(
                            [('state', '=', 'd')])
                rec.draft_count =draft

            elif rec.name == "Online Sales":
                draft =self.env['custom.quality.check'].search_count(
                            [('state', '=', 'd'),('is_online_sale','=',True)])
                rec.draft_count =draft

            else:
                draft = self.env['moqc.check'].search_count(
                    [('state', '=', 'd')])
                rec.draft_count = draft

    def _compute_pending_count(self):
        for rec in self:
            if rec.name == "GRN QC":
                pending =self.env['custom.quality.check'].search_count(
                            [('state', '=', 'o')])
                rec.pending_count =pending

            elif rec.name == "Online Sales":
                pending =self.env['custom.quality.check'].search_count(
                            [('state', '=', 'o'),('is_online_sale','=',True)])
                rec.pending_count =pending

            else:
                pending = self.env['moqc.check'].search_count(
                    [('state', '=', 'o')])
                rec.pending_count = pending

    def _compute_completed_count(self):
        for rec in self:
            if rec.name == "GRN QC":
                compltete =self.env['custom.quality.check'].search_count(
                            [('state', '=', 'c')])
                rec.completed_count =compltete

            elif rec.name == "Online Sales":
                compltete =self.env['custom.quality.check'].search_count(
                            [('state', '=', 'c'),('is_online_sale','=',True)])
                rec.completed_count =compltete

            else:
                compltete = self.env['moqc.check'].search_count(
                    [('state', '=', 'c')])
                rec.completed_count = compltete





    def get_action_picking_tree_ready(self):
        if self.name=="GRN QC":
            # print("GRN")

            action =self.env.ref('quality_check.action_view_quality').read()[0]
            action['domain'] = [('state','=','d')]
            return action

        if self.name=="MOQC":
            # print("MOQC")
            action = self.env.ref('quality_check.action_view_moqc').read()[0]
            action['domain'] = [('state', '=', 'd')]
            return action

        if self.name=="Online Sales":
            # print("MOQC")
            action = self.env.ref('quality_check.action_view_quality').read()[0]
            action['domain'] = [('state', '=', 'd'),('is_online_sale','=',True)]
            return action

    def get_qc_tree_completed(self):
        if self.name == "GRN QC":
            # print("GRN")
            action = self.env.ref('quality_check.action_view_quality').read()[0]
            action['domain'] = [('state', '=', 'c')]
            return action

        if self.name == "MOQC":
            # print("MOQC")
            action = self.env.ref('quality_check.action_view_moqc').read()[0]
            action['domain'] = [('state', '=', 'c')]
            return action

        if self.name=="Online Sales":
            # print("MOQC")
            action = self.env.ref('quality_check.action_view_quality').read()[0]
            action['domain'] = [('state', '=', 'c'),('is_online_sale','=',True)]
            return action

    def get_qc_tree_processing(self):
        if self.name == "GRN QC":
            # print("GRN")
            action = self.env.ref('quality_check.action_view_quality').read()[0]
            action['domain'] = [('state', '=', 'o')]
            return action

        if self.name == "MOQC":
            # print("MOQC")
            action = self.env.ref('quality_check.action_view_moqc').read()[0]
            action['domain'] = [('state', '=', 'o')]
            return action

        if self.name=="Online Sales":
            # print("MOQC")
            action = self.env.ref('quality_check.action_view_quality').read()[0]
            action['domain'] = [('state', '=', 'o'),('is_online_sale','=',True)]
            return action