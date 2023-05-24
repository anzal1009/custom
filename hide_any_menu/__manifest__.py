# -*- coding: utf-8 -*-
{
    'name': 'Hide Any Menu, Any Field, Any Report, Any Button',

    'summary': 'Hide Any Field Hide Any Report hide any button From Any User Generic Security Restriction generic_security_restriction restrict menu show_hide_menu hide menu hide field hide report hide button hide user menus User Menu Restriction Security for Menu',
    'description': """
        
        """,

    'author': "Ideenkreise Tech Pvt Ltd",
    'website': "https://www.ideenkreisetech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [

        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
