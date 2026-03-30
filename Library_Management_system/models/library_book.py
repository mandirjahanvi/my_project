from odoo import models, fields,api

class library_book(models.Model):
    _name='library.book'
    _rec_name = 'name'

    name=fields.Char("Name")
    author=fields.Char("author")
    available_qty=fields.Integer("Available Qty")
    is_available=fields.Boolean("Is Available",compute='compute_is_available',store=True)

    @api.depends('available_qty')
    def compute_is_available(self):
        for book in self:
            book.is_available=book.available_qty>0
