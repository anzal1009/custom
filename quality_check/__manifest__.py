{''
 'name': 'Quality Check ',
 'summary': """Custom for ERP""",
 'version': '0.1',
 'sequence':'-660',
 'description': """API for ERP""",
 'author': 'Ideenkreise Tech Pvt Ltd',
 'company': 'Ideenkreise Tech Pvt Ltd',
 'website': 'https://www.ideenkreisetech.com',
 'category': 'Tools',
  'depends': ['mrp','account','sale','purchase','stock'],
 'license': 'AGPL-3',
 'data': [
'security/ir.model.access.csv',
'security/groups.xml',
'report/report.xml',
'report/poqc_report.xml',
'report/moqc_report.xml',
'wizard/moqc_check.xml',
'data/data.xml',
# 'wizard/check.xml'
# 'views/purchase.xml',
'views/overview.xml',
'views/quality_check.xml',
'views/moqc_check.xml',
'views/params.xml',
'views/moqc.xml',
# 'views/mo_fail.xml',
# 'views/po_fail.xml',
'views/transfer_inherit.xml',
'views/mo_inherit.xml',
# 'views/report.xml',
# 'views/qc_rm.xml',
'demo/demo.xml',



        ],
 'demo': ['demo/demo.xml'],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
