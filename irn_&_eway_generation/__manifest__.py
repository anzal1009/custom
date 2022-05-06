{''
 'name': 'IRN & EWAY Generation',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-60',
 'description': """IRN for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['account','mrp','base_accounting_kit'],
 'license': 'AGPL-3',
 'data': [

'views/eway_bill.xml',
'views/main_irn.xml',

          ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
