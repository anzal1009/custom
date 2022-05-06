# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Import Manufacturing Order',
    'version': '15.0.1.0',
    'license': 'OPL-1',
    'summary': 'Import Manufacturing Order using CSV and Excel files.',
    'category': 'Mrp',
    'description': """"
        Import Manufacturing Order using CSV and Excel files.
    """,
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com',
    'depends': ['mrp', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_manufacturing_order_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'price': 09.00,
    'currency': 'EUR',
    'qweb': [],
}
