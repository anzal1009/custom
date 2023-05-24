
{
    'name': "Restrict Concurrent User Login",
    'version': '14.0.1.1.2',
    'summary': 'Restrict concurrent sessions, User force logout, Automatic session expiry',
    "description": """Restrict concurrent sessions, User force logout, Automatic session expiry, 
                      restrict user login, session expiry, session, user session, force logout,
                      automatic expiry""",
    'author': 'Primera Solutions',
    'company': 'Primera Solutions',
    'maintainer': 'Primera Solutions',
    'website': "https://www.primera.solutions",
    'depends': ['base'],

    'data': [
        'data/data.xml',
        'views/res_users_view.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
