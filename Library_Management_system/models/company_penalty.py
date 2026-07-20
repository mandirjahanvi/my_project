from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    penalty_charge = fields.Float("Penalty Charge")
    book_validity = fields.Integer("Book Validity Days",default=30)
    penalty_range = fields.One2many('penalty.range',"company_id",string="Penalty Range")
    issue_picking_id = fields.Many2one('stock.picking.type',string="Issue Picking")
    return_picking_id = fields.Many2one( 'stock.picking.type',string="Return Picking")