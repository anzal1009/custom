{''
 'name': 'Invoice Reports ',
 'summary': """Custom Fields for ERP""",
 'version': '0.1',
 'sequence':'-990',
 'description': """Invoice reports""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['sale_management','purchase','account','stock'],
 'license': 'AGPL-3',
 'data': [
'report/report.xml',
'report/customs_invoice.xml',
'report/customer_invoice.xml',
'report/inherit_delivery_slip.xml',
# 'report/customer_invoice1.xml',
'views/invoice_reports.xml',


          ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
