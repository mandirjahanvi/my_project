from odoo import models, fields,api

class transaction(models.Model):
    _name = 'bank.transaction'
    _rec_name = 'customer_id'

    bank_id=fields.Many2one('bank.account',"Account")
    customer_id=fields.Many2one('customer.master',"Customer",domain="[('id','=',customer_details)]")
    amount=fields.Float('Amount')
    date=fields.Date('Date',default=lambda self:fields.Date.context_today(self))
    transaction_type=fields.Selection([('credit','Deposit'),('debit','Withdraw')],"Transaction Type")
    customer_details=fields.Many2one('customer.master',related='bank_id.customer_id')

    @api.onchange('bank_id')
    def onchange_bank_id(self):
        self.customer_id=self.bank_id and self.bank_id.customer_id.id or False

