{''
 'name': 'Date Confirmation',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-60',
 'description': """Custom for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['stock','base','sale','purchase'],
 'license': 'AGPL-3',
 'data': [
'security/ir.model.access.csv',
 # 'wizard/date_validate_wizard.xml',
 'views/date_validate.xml',
        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
