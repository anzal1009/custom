{''
 'name': 'Manufacturing Order Upload without BOM',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-60',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp'],
 'license': 'AGPL-3',
 'data': [
'security/ir.model.access.csv',
 'wizard/mo_upload.xml',
 # 'views/mo_line_custom.xml',
        ],
'images': ['static/description/banner.jpg'],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
