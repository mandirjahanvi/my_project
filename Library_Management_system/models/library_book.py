from odoo import models, fields,api

class library_book(models.Model):
    _name='library.book'

    name=fields.Char("Name")
    author=fields.Char("author")
    available_qty=fields.Integer("Available Qty")
    is_available=fields.Boolean("Is Available",compute='compute_is_available',store=True)
    photo=fields.Binary("Photo",widget="image")
    code=fields.Char("Code")
    issue_book_count=fields.Integer("Issue count",compute="compute_issue_count")
    display_name = fields.Char(compute="_compute_display_name", store=True)


    @api.depends('available_qty')
    def compute_is_available(self):
        for book in self:
            book.is_available=book.available_qty>0

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for book in self:
            if book.code:
                book.display_name = f"[{book.code}] {book.name}"
            else:
                book.display_name = book.name

    def compute_issue_count(self):
        for book in self:
            book.issue_book_count = self.env['book.issue.line'].search_count([
                ('book_id', '=', book.id)])

    def action_view_issues(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Issues',
            'res_model': 'book.issue',
            'view_mode': 'list,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'default_book_id': self.id},
        }
