# -*- coding: utf-8 -*-
{
    'name': "Restrict UoM Creation and Updation",

    'summary': """
        Restrict UoM creation and updation""",

    'description': """
        Restrict UoM creation and updation
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
    'depends': ['base', 'uom'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/uom_security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
