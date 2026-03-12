from odoo import models,fields

class bank_account(models.Model):
    _name = 'bank.account'
    _rec_name = 'acc_no'

    acc_no = fields.Char('Account Number')
    balance = fields.Float('Balance')
    bank_name = fields.Char('Bank Name')
    account_type=fields.Selection([('saving','Saving'),('current','Current')],string='Account Type',default='current')
    ifsc_code = fields.Char('IFSC Code')
    customer_id=fields.Many2one('customer.master',string='Customer')
    tag_id = fields.Many2many('bank.account.tags', 'bank_acc_tag_rel', 'bank_id', 'tag_id')

class bank_acc_tags(models.Model):
    _name = 'bank.account.tags'

    name = fields.Char('Tag Name')
    acc_name = fields.Many2many(
        'bank.account',
        'bank_acc_tag_rel',
        'tag_id',
        'bank_id',
        string='Accounter Name'
    )
