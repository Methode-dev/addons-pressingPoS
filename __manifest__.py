{
    'name': 'Pressing - Point of Sale',
    'version': '19.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'author': 'Méthode',
    'website': 'https://methode.dev',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/laundry_treatment_data.xml',
        'views/laundry_treatment_views.xml',
        'views/product_views.xml',
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_pressing_methode/static/src/app/**/*.js',
            'pos_pressing_methode/static/src/app/**/*.xml',
            'pos_pressing_methode/static/src/scss/*.scss',
        ],
    },
    'installable': True,
}
