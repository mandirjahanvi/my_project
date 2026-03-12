from odoo import models, fields,api

class customer(models.Model):
    _name = 'customer.master'

    name=fields.Char('Name')
    address=fields.Char('Address')
    email=fields.Char('Email')
    phone=fields.Char('Phone')
    account_ids=fields.One2many('bank.account','customer_id',string='Bank Accounts')
    state_name = fields.Selection([
        ('gujarat', 'Gujarat'),
        ('goa', 'Goa'),
        ('punjab', 'Punjab'),
        ('rajasthan', 'Rajasthan'),
        ('delhi', 'Delhi'),
        ('maharashtra', 'Maharashtra'),
    ], string='State', default='gujarat')




