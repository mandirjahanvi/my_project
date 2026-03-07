
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hospital Management',
    'summary': 'Hospital Appointment Manages',
    'description': 'Hospital Appointment Manages',
    'depends': ['base'],
    'data': ['security/security.xml',
        'security/ir.model.access.csv',
        'views/doctor.xml','views/patient.xml','views/appointment.xml'],
    'installable': True,
    'application': True,

}