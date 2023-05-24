# -*- coding: utf-8 -*-
{
    'name': "default_invoice_print",

    'summary': """
         
      """,

    'description': """
       Add vehicle number in invoice and default invoice print. Set vehicle number is required.
       And remove internal referance in print. 
    """,

    'author': "LOYAL IT SOLUTIONS",
    'website': "https://www.loyalitsolutions.com/",
    'category': 'account',
    'version': '15.0.1',
    'license': 'LGPL-3',

    'depends': ['base', 'account', 'l10n_in', 'sale'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
