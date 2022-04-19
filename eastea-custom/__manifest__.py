{''
 'name': 'Eastea Custom',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-60',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['sale_management','purchase','account','purchase_order_automation_lot_import','bi_create_single_invoice'],
 'license': 'AGPL-3',
 'data': [
  'reports/report.xml',
  'reports/sales_order.xml',
  'reports/purchase_order.xml',
  'reports/vendor_bill.xml',
  'reports/customer_invoice.xml',
  'views/button_inherit.xml',



          ],
 'demo': [],
 'images': ['static/description/icon.png'],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
