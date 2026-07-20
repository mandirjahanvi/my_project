from odoo import models, fields , api
from odoo.exceptions import UserError


class LibraryPenaltyPayment(models.Model):
    _name = 'library.penalty.payment'
    _description = 'Library Penalty Payment'
    _rec_name = 'reference'

    reference = fields.Char(default='New',readonly=True,copy=False)
    issue_id = fields.Many2one('book.issue',string='Book Issue',required=True)
    member_id = fields.Many2one('library.member',string='Member',related='issue_id.member_id',store=True)
    amount = fields.Float(string='Amount',required=True)
    payment_date = fields.Date(default=fields.Date.today)
    payment_method = fields.Selection([('cash', 'Cash'),('upi', 'UPI'),('card', 'Card')], default='cash')
    state = fields.Selection([('draft', 'Draft'),('paid', 'Paid')],string="Status", default='draft',readonly="1")

    @api.model
    def create(self,vals):
        if vals.get('reference','New')=='New':
            vals['reference'] =self.env['ir.sequence'].next_by_code('library.penalty.payment') or 'New'
            return super().create(vals)

    def action_confirm_payment(self):
        self.ensure_one()
        if self.amount <= 0:
            raise UserError("Payment amount must be greater than zero.")
        self.state = 'paid'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'library.penalty.payment',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_print_receipt(self):
        self.ensure_one()
        return self.env.ref(
            'library_management_system.action_report_penalty_receipt'
        ).report_action(self)