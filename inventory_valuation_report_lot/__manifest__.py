{''
 'name': 'Stock Lot Valuation',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-14560',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','stock','purchase','sale'],
 'license': 'AGPL-3',
 'data': [
# 'security/ir.model.access.csv',
'views/lot.xml',
# 'views/stock_value.xml',
# 'views/stock_qty.xml',
        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
