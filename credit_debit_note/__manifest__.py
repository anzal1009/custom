{''
 'name': 'Credit/Debit Note Customization',
 'summary': """Custom Fields for ERP""",
 'version': '0.1',
 'sequence':'-110',
 'description': """Custom For Reports""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['account','stock','sale','purchase'],
 'license': 'AGPL-3',
 'data': [

# 'views/mo_bt.xml',
'reports/report.xml',
 'reports/credit_note.xml',


          ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }