from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    author = fields.Char("Author")
    is_book = fields.Boolean("Is Book",default=True)
    is_available = fields.Boolean("Is Available", compute='_compute_is_available', store=False)
    issue_book_count = fields.Integer("Issue count", compute="compute_issue_count")
    issue_id=fields.One2many("book.issue.line",'book_id',string='Issue Lines')

    @api.depends('qty_available')
    def _compute_is_available(self):
        for book in self:
            book.is_available = book.qty_available > 0

    def compute_issue_count(self):
        for book in self:
            book.issue_book_count = self.env['book.issue.line'].search_count([
                ('book_id.product_tmpl_id', '=', book.id)])

    def action_view_issues(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Issues',
            'res_model': 'book.issue',
            'view_mode': 'list,form',
            'domain': [('book_line_ids.book_id.product_tmpl_id', '=', self.id)],
        }
