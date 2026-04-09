from odoo import models, fields,api
from odoo.exceptions import UserError
from datetime import timedelta


class book_issue(models.Model):
    _name = 'book.issue'
    _description ='Book Issue'

    book_id=fields.Many2one('library.book','Book Name')
    member_id=fields.Many2one('res.users','Member')
    issue_date=fields.Date('Issue Date',default=fields.Date.today)
    return_date=fields.Date('Return Date')
    status=fields.Selection([('draft','Draft'),('issued','Issued'),('returned','Returned')],string='Status',default='draft')
    days_issued = fields.Integer("Days Issued",compute="_compute_book",store=True)
    last_date_of_return=fields.Date("Last Date")
    penalty=fields.Float("Penalty",compute="compute_penalty")

    @api.depends('issue_date', 'return_date')
    def _compute_book(self):
        for book in self:
            if book.issue_date:
                end_date = book.return_date or fields.Date.today()
                book.days_issued = max((end_date - book.issue_date).days, 0)
            else:
                book.days_issued = 0

    def action_issue_book(self):
        for book in self:
            if book.status == 'draft':
                if book.book_id.available_qty <= 0:
                    raise UserError("No books available to issue!")
                company=self.env.company
                if company.book_validity:
                    book.last_date_of_return = book.issue_date + timedelta(days = company.book_validity)
                book.status = 'issued'
                book.book_id.available_qty -= 1
            else:
                raise UserError("Book is already issued or returned!")


    @api.depends('return_date', 'last_date_of_return')
    def compute_penalty(self):
        company = self.env.company
        for book in self:
            book.penalty = 0
            if book.return_date and book.last_date_of_return and book.return_date > book.last_date_of_return:
                delay = book.return_date - book.last_date_of_return
                delay_days = max(delay.days, 0)
                penalty_amt = company.penalty_charge or 0
                record = self.env['penalty.range'].search([('from_day', '<=', delay_days),('to_day', '>=', delay_days),('company_id', '=', self.env.company.id)],limit=1)
                penalty_percentage = record.penalty_range if record else 0
                book.penalty = penalty_amt + (penalty_amt * (penalty_percentage / 100))

    def action_update_return(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Return Date',
            'res_model': 'return.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_book_issue_id': self.id,
                'default_return_date': self.return_date,
            }
        }

    def action_return_book(self):
        for book in self:
            if book.status != 'issued':
                raise UserError("Book must be issued before returning!")
            book.write({'return_date': fields.Date.today(),
                        'status': 'returned'})
            book.book_id.available_qty += 1




