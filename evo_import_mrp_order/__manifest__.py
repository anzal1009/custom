# -*- coding: utf-8 -*-
{
    'name': 'Manufacturing Order Import',
    'summary': 'Import Manufacturing Order, MO Import, Import data from Excel',
    'category': 'Manufacturing/Manufacturing',
    'version': '15.0.1.0',
    'author': 'Evozard',
    'license': 'OPL-1',
    'price': 25,
    'currency': 'USD',
    'support':'support@evozard.com',    
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'security/import_mrp_security.xml',
        'wizards/import_mrp_wizard.xml',
    ],
    'images': ["static/description/banner.gif"],    
    'installable': True,
    'auto_install': False,
    'application': True,
}
