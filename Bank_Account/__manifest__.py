# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Bank Account',
    'summary': 'Bank Account Manages',
    'description': 'Bank Account Manages',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml'],
    'installable': True,
    'application': True,

}