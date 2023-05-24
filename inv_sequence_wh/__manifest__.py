# -*- coding: utf-8 -*-
{
    'name': "Invoice Sequence based on Warehouse ",

    'summary': """
        Sequence of invoice based on warehouse selected in invoice and company address in invoice print as warehouse address""",

    'description': """
        Sequence of invoice based on warehouse selected in invoice and company address in invoice print as warehouse address
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "http://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock', 'default_invoice_print', 'web', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
