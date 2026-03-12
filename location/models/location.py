from odoo import models, fields

class Location(models.Model):
    _name = 'bank.location'
    _rec_name = 'bank_name'

    bank_name = fields.Char(string="Bank Name",required=True)
    city_id = fields.Many2many('bank.city',string="cities")