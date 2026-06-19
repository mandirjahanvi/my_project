from odoo import api, fields, models
from datetime import date

class LibraryDashboard(models.Model):
    _name = 'library.dashboard'
    _description = 'Library Dashboard'

    total_books = fields.Integer("Total Books")
    total_members = fields.Integer("Total Members")
    issued_books = fields.Integer("Issued Books")
    overdue_books =fields.Integer("overdue_books")

    @api.model
    def get_dashboard_data(self):

        total_books = self.env['product.product'].search_count([('is_book', '=', True)])
        total_members = self.env['library.member'].search_count([])
        issued_books = self.env['book.issue'].search_count([('status', '=', 'issued')])
        returned_books = self.env['book.issue'].search_count([('status', '=', 'returned')])

        today=date.today()
        overdue_books = self.env['book.issue.line'].search_count([
            ('last_date_of_return', '<', today),

        ])
        recent_issue_lines = self.env['book.issue.line'].search([],limit=5,order='issue_date desc')
        recent_issues = []
        for rec in recent_issue_lines:
            recent_issues.append({
                'member': rec.issue_id.member_id.user_id.display_name,
                'book': rec.book_id.name,
                'issue_date': rec.issue_date.strftime('%d-%m-%Y')
                if rec.issue_date else '',
                'due_date': rec.last_date_of_return.strftime('%d-%m-%Y')
                if rec.last_date_of_return else '',
                'status': rec.issue_id.status,
                'penalty': rec.penalty,
            })
        overdue_lines = self.env['book.issue.line'].search([
            ('last_date_of_return', '<', today),
            ('returned', '=', False)
        ], limit=5)
        overdue_data = []
        for rec in overdue_lines:
            overdue_days = (today - rec.last_date_of_return).days
            overdue_data.append({
                'member': rec.issue_id.member_id.name,
                'book': rec.book_id.name,
                'due_date': rec.last_date_of_return.strftime('%d-%m-%Y')
                if rec.last_date_of_return else '',
                'days_overdue': overdue_days,})
        return {
            'total_books': total_books,
            'total_members': total_members,
            'issued_books': issued_books,
            'returned_books': returned_books,
            'overdue_books': overdue_books,
            'recent_issues': recent_issues,
            'overdue_data': overdue_data,
        }