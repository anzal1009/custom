{''
 'name': 'Purchase Report',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-1110',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','account','sale','purchase','stock'],
 'license': 'AGPL-3',
 'data': [

'report/purchase_inherit.xml',

        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }