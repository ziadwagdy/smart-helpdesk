{
    'name': 'Smart Helpdesk - AI',
    'version': '17.0',
    'category': 'Helpdesk',
    'summary': 'Smart Helpdesk Module for Odoo 17',
    'sequence': 10,
    'license': 'LGPL-3',
    'author': 'ziadwagdy',
    'website': 'https://github.com/ziadwagdy',
    'depends': ['base', 'helpdesk'],
    'data': [
        # Add your xml, csv files here. For example,
        # 'views/helpdesk_view.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}