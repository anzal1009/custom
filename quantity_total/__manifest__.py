{''
 'name': 'Line Total Qunatity',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-2000',
 'description': """Total quantity of line items""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['base','account','sale','purchase','stock'],
 'license': 'AGPL-3',
 'data': [
 'reports/qty_subtotal.xml',
 'reports/purchase_qty.xml',
 'reports/invoice_qty.xml',
 'reports/delivery_slip.xml',
'views/subtotal_qty.xml',

        ],
'images': ['static/description/icon.png'],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
