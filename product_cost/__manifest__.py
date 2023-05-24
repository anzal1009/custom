{''
 'name': 'Cost Button',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-880',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','stock','purchase'],
 'license': 'AGPL-3',
 'data': [
'security/ir.model.access.csv',
'wizard/cost_wizrd.xml',
'views/cost_button.xml',
        ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }