from odoo import models, fields,api
from odoo.exceptions import UserError
from datetime import timedelta


class book_issue(models.Model):
    _name = 'book.issue'
    _rec_name = 'book_id'

    book_id=fields.Many2one('library.book','Book')
    member_id=fields.Many2one('res.users','Member')
    issue_date=fields.Date('Issue Date')
    return_date=fields.Date('Return Date')
    status=fields.Selection([('draft','Draft'),('issued','Issued'),('returned','Returned')],string='Status',default='draft')
    days_issued = fields.Integer("Days Issued",compute="_compute_book",store=True)
    last_date_of_return=fields.Date("Last Date")
    penalty=fields.Integer("Penalty",compute="compute_penalty",store=True)

    @api.depends('issue_date', 'return_date')
    def _compute_book(self):
        for book in self:
            if book.issue_date:
                end_date = book.return_date or fields.Date.today()
                days = max((end_date - book.issue_date).days, 0)
                book.days_issued = days
            else:
                book.days_issued = 0

    def action_issue_book(self):
        for book in self:
            if book.status == 'draft':
                if book.book_id.available_qty <= 0:
                    raise UserError("No books available to issue!")
                company=self.env.company
                book.issue_date = fields.Date.today()
                if company.book_validity:
                    book.last_date_of_return = book.issue_date + timedelta(days = company.book_validity)
                book.status = 'issued'
                book.book_id.available_qty -= 1
            else:
                raise UserError("Book is already issued or returned!")

    @api.depends('return_date', 'last_date_of_return')
    def compute_penalty(self):
        for book in self:
            p = 0
            company = self.env.company
            if book.return_date and book.last_date_of_return:
                if book.return_date > book.last_date_of_return:
                    p = company.penalty_charge
            book.penalty = p

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
            book.write({'return_date':fields.Date.today(),'status':'returned'})
            book.book_id.available_qty += 1


