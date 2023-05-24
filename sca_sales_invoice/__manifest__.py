{''
 'name': 'SCA Sales Invoice',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-1110',
 'description': """Custom for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','account','sale','purchase','stock'],
 'license': 'AGPL-3',
 'data': [
'reports/reports.xml',
'reports/sales_invoice.xml',
'views/address.xml',

        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
