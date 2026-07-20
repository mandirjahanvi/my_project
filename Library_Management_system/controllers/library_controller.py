import json
from odoo import http
from odoo.http import request

class CustomerAPI(http.Controller):

    @http.route('/api/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_book(self):
        book = request.env['library.book'].sudo().search([])

        data = []
        for b in book:
            data.append({
                "Book_name": b.name,
                "Author_name": b.author,
            })

        return request.make_response(
            json.dumps({
                "status": "success",
                "data": data
            }),
            headers=[('Content-Type', 'application/json')]
        )