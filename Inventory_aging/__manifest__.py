{''
 'name': 'Inventory Aging Reprt',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-14562',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['stock'],
 'license': 'AGPL-3',
 'data': [
'report/report.xml',
'report/inventory_aging.xml',
'wizard/invntry_aging.xml',
'security/ir.model.access.csv',
# 'views/view.xml',


        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
