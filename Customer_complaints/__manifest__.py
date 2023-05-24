{''
 'name': 'Customer Complaints ',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-60',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','account','sale','purchase'],
 'license': 'AGPL-3',
 'data': [
'security/ir.model.access.csv',
'data/data.xml',

'reports/reports.xml',
'reports/complaint.xml',
'views/complaint.xml',
'data/mail_template.xml',
'data/mail_confirm.xml',
        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
