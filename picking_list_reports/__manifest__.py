{''
 'name': 'Picking list Reports',
 'summary': """Custom Fields for ERP""",
 'version': '0.1',
 'sequence':'-2990',
 'description': """Picking list reports""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['sale_management','purchase','account','stock','sale','product'],
 'license': 'AGPL-3',
 'data': [
'report/report.xml',
'report/packing_list_customer.xml',
'report/packing_list_customs.xml',
'views/packing_list.xml',
'views/packing_line.xml',

          ],
 'demo': [],

 'installable': True,
 'auto_install': False,
 'application' : True
 }
