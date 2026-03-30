from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    penalty_charge = fields.Float(string="Penalty Charge")
    book_validity = fields.Integer(string="Book Validity Days",default=30)