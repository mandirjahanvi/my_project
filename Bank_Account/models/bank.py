from odoo import models,fields,api

class bank_account(models.Model):
    _name = 'bank.account'
    _rec_name = 'acc_no'

    acc_no = fields.Char('Account Number')
    balance = fields.Float('Balance')
    account_type=fields.Selection([('saving','Saving'),('current','Current')],string='Account Type',default='current')
    customer_id=fields.Many2one('customer.master',string='Customer')
    tag_id = fields.Many2many('bank.account.tags', 'bank_acc_tag_rel', 'bank_id', 'tag_id',string="Tags")
    balance_compute = fields.Float(compute='calculate_balance',string="Balance",store=True)
    transaction_ids = fields.One2many('bank.transaction','bank_id',string="Transactions")

    @api.depends('transaction_ids','transaction_ids.bank_id','transaction_ids.amount','transaction_ids.transaction_type')
    def calculate_balance(self):
        for i in self:
            balance = 0
            for transaction in i.transaction_ids:
                if transaction.transaction_type == 'credit':
                    balance = balance + transaction.amount
                else:
                    balance = balance - transaction.amount
            i.balance_compute = balance


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
