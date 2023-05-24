{''
 'name': 'Warehouse Invoice',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-10000',
 'description': """Custom for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','account','sale','purchase','stock'],
 'license': 'AGPL-3',
 'data': [
'reports/report.xml',
'reports/sale_invoice.xml',
'reports/acc_invoice.xml',
'views/warehouse.xml',
'views/users.xml',

        ],
'images': ['static/description/icon.png'],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
