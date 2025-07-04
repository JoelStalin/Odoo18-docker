{   'assets': {   'point_of_sale.assets': [   'l10n_do_pos/static/src/scss/ui_autocomplete.scss',
                                              'l10n_do_pos/static/src/css/pos.css',
                                              'l10n_do_pos/static/src/js/models.js',
                                              'l10n_do_pos/static/src/js/Screens/ClientDetailsEdit.js',
                                              'l10n_do_pos/static/src/js/Screens/PaymentScreen.js',
                                              'l10n_do_pos/static/src/js/Screens/TicketScreen.js',
                                              'l10n_do_pos/static/src/js/Screens/OrderWidget.js',
                                              'l10n_do_pos/static/src/js/Screens/ClientListScreen.js'],
                  'web.assets_qweb': ['l10n_do_pos/static/src/xml/**/*']},
    'author': 'Joel S. Martinez espinal',
    'category': 'Localization',
    'data': [   'data/pos_payment_method_data.xml',
                'data/account_fiscal_position_data.xml',
                'security/ir.model.access.csv',
                'data/res_partner_data.xml',
                'views/pos_config_view.xml',
                'views/account_fiscal_position_views.xml',
                'views/pos_order_view.xml'],
    'depends': [   'base',
                   'l10n_do_accounting',
                   'point_of_sale',
                   'l10n_do_rnc_search'],
    'license': 'LGPL-3',
    'maintainers': ['Joel S. Martinez espinal'],
    'name': 'DO Accounting POS',
    'post_init_hook': '_l10n_do_pos_post_init',
    'version': '18.0.1.0.0',
    'website': 'https://neotec.do/'}