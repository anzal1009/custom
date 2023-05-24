{''
 'name': 'User Access Restriction for Pricelist',
 'summary': """Custom Access for ERP""",
 'version': '0.1',
 'sequence':'-580',
 'description': """Custom Access Rights""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['account','mrp','base','stock','base_accounting_kit','sale'],
 'license': 'AGPL-3',
 'data': [
'security/group.xml',
'views/views.xml',

          ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
