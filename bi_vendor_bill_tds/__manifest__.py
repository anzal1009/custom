# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Vendor Bill TDS for Indian Localization',
    'version': '15.0.0.0',
    'category': 'Purchase',
    'summary': 'Apply TDS on vendor bill TDS amount on invoice deduct TDS on payment apply TDS on invoice Indian TDS for Indian Accounting TDS cut TDS amount on vendor Payment TDS supplier invoice with TDS vendor payment with TDS account deduct TDS from vendor payment',
    'description': """

            Vendor Bill TDS for Indian Localization in Odoo,
            Vendor bill TDS in odoo,
            Calculate TDS amount on percentage in odoo,
            Apply TDS checkbox in odoo,
            Select TDS account for vendor bill in odoo,
            TDS amount on vendor bill in odoo,


    """,
    'author': 'BrowseInfo',
    'price': 25,
    'currency': "EUR",
    'website': 'https://www.browseinfo.in',
    'depends': ['sale_management', 'purchase','account'],
    'data': [
            'views/account_view.xml',
            'reports/inherit_account_report.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url':'https://youtu.be/Yu2fPhCZ020',
    "images":['static/description/Banner.png'],
    'license': 'OPL-1',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
