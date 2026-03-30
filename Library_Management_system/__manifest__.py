{
    'name': 'Library Management',
    'summary': 'Library Management System',
    'description': 'Library Management System',
    'depends': ['base'],
    'data': [
                'security/security.xml',
                'security/ir.model.access.csv',
                'views/library_book.xml',
                'views/book_issue.xml',
                'views/penalty.xml',
                'wizard/view.xml',

    ],
    'installable': True,
    'application': True,

}