from odoo import api,models,fields


class QualityCheck(models.Model):
    _name = "quality.check"

    name = fields.Many2one('product.template', string='Product')
    team = fields.Many2one('quality.team', string='Quality Team')


    # qc = fields.Many2many('quality.product.lines',string='Analysis')

    data1 = fields.One2many('quality.check.lines1', 'data', string='Sale')


    # @api.model
    # def default_get(self, fields_list):
    #     res = super(QualityCheck, self).default_get(fields_list)
    #     print('eee')
    #     return res

    # @api.model
    # def default_get(self, fields):
    #     res = super(QualityCheck, self).default_get(fields)
    #     data1 = []
    #     product_rec = self.env['quality.product'].search([])
    #     for pro in product_rec:
    #         line = (0, 0, {
    #             'attribute': pro.name,
    #
    #         })
    #         data1.append(line)
    #     res.update({
    #         'data1': data1,
    #
    #         # 'notes': 'Like and Subscribe our channel To Get Notified'
    #     })
    #     return res







class QualityCheck(models.Model):
    _name = "quality.check.lines1"

    attribute = fields.Many2one('quality.product',string='Characters')
    good = fields.Boolean(string='Pass')
    avg = fields.Boolean(string="Fail")

    data = fields.Many2one('quality.check', string='Data')
