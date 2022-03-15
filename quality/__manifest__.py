{''
 'name': 'Quality Check',
 'summary': """This module will add a record to store quality details""",
 'version': '10.0.1.0.0',
'sequence':'-60',
 'description': """This module will add a record to store quality details""",
 'author': 'Anzal',
 'company': 'Cybrosys Techno Solutions',
 'website': 'https://www.cybrosys.com',
 'category': 'Tools',
 'depends': ['stock'],
 'license': 'AGPL-3',
 'data': ['security/ir.model.access.csv',
 'views/test_team.xml',
 'views/product_qc.xml',
 'views/quality_check.xml',

          ],
 'demo': [],
 'installable': True,
 'auto_install': False,
 'application' : True
 }
