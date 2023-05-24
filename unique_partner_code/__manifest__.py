# -*- coding: utf-8 -*-
{
    'name': "Unique Partner Code",

    'summary': """
        Unique vendor code and customer code based on type of partner""",

    'description': """
        Unique vendor code and customer code based on type of partner
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'is_customer_vendor', 'sale', 'purchase', 'account', 'bi_sale_purchase_discount_with_tax'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
