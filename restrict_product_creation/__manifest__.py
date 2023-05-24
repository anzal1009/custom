# -*- coding: utf-8 -*-
{
    'name': "Restrict Product Creation and Updation",

    'summary': """
        Restrict product creation and updation""",

    'description': """
        Restrict product creation and updation
    """,

    'author': "ACCESS",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/product_security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
