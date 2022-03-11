from odoo import models, fields


class QualityCheck(models.Model):
    _name = "quality.product"

    # name = fields.Char(string='Character')
    name = fields.Char(string='Test Name')
    rem = fields.Char(string='Remarks')


    # class QualityCheck1(models.Model):
    #     _name = "quality.product.lines"
    #
    #     attribute = fields.Char(string='Characters')
    #     good = fields.Char(string='Values')
    #     avg = fields.Char(string="Rating")
    #
    #     data = fields.Many2one('quality.product', string='Data')
