{   'application': True,
    'assets': {   'web.assets_backend': [   '/web_digital_sign/static/src/js/digital_sign.js',
                                            '/web_digital_sign/static/src/xml/digital_sign.xml']},
    'author': 'Joel S. Martinez espinal',
    'category': 'Tools',
    'data': ['views/account_move_view.xml', 'views/res_partner_view.xml'],
    'depends': ['web', 'account', 'exo_api'],
    'description': '\n'
                   '     This module provides the functionality to store '
                   'digital signature\n'
                   "     Example can be seen into the User's form view where "
                   'we have\n'
                   '        added a test field under signature.\n'
                   '    ',
    'images': ['static/description/Digital_Signature.jpg'],
    'installable': True,
    'license': 'LGPL-3',
    'maintainers': ['Joel S. Martinez espinal'],
    'name': 'Web Digital Signature',
    'sequence': 3,
    'summary': '\n'
               '        Touch screen enable so user can add signature with '
               'touch devices.\n'
               '        Digital signature can be very usefull for documents.\n'
               '    ',
    'version': '18.0.1.0.0',
    'website': 'http://www.serpentcs.com/'}