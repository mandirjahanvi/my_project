from odoo import fields, models

class city(models.Model):
    _name = 'bank.city'
    _rec_name = 'city_name'

    city_name = fields.Char(string="City Name",required=True)
    bank_id = fields.Many2many('bank.location',string="Bank")