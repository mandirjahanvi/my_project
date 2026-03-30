from odoo import models,api,fields

class ReturnDateWizard(models.TransientModel):
    _name = 'return.date.wizard'
    _description = 'Update Return Date'

    return_date = fields.Date("Return Date", required=True)
    book_issue_id = fields.Many2one('book.issue', string="Book")

    def action_confirm(self):
        self.book_issue_id.write({
            'return_date': self.return_date,
        })
