{''
 'name': 'Sale Order Lot No Upload',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-60',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['sale'],
 'license': 'AGPL-3',
 'data': [
'security/ir.model.access.csv',
 'wizard/sale_lot_no_wiz.xml',
 'views/sale_lot_no.xml',
        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
