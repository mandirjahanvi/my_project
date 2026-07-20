{
    'name': 'Library Management',
    'summary': 'Library Management System',
    'description': 'Library Management System',
    'depends': ['base','product','stock'],
    'data': [
                'security/security.xml',
                'security/ir.model.access.csv',

                'data/library_penalty_payment_sequence.xml',

                'views/dashboard_view.xml',
                'views/inventory_book.xml',
                'views/book_issue.xml',
                'views/penalty.xml',
                'views/library_penalty_payment_views.xml',
                'views/library_member_views.xml',
                'views/action.xml',
                'wizard/view.xml',
                'views/menu.xml',

                'report/member_history_report.xml',
                'report/report.xml',
                'report/report_penalty_receipt.xml',
                'report/report_penalty_receipt_template.xml',
    ],

        'assets': {
            'web.assets_backend': [
                'library_management_system/static/src/js/dashboard.js',
                'library_management_system/static/src/xml/dashboard.xml',
                'library_management_system/static/src/scss/dashboard.scss',
            ],},
    'installable': True,
    'application': True,

}