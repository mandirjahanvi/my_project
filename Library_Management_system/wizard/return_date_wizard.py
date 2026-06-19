from odoo import models,api,fields
from odoo.exceptions import UserError


class ReturnDateWizard(models.TransientModel):
    _name = 'return.date.wizard'
    _description = 'Update Return Date'

    return_date = fields.Date("Return Date", required=True)
    issue_line_id = fields.Many2one('book.issue.line', string="Book")

    def action_confirm(self):
        self.ensure_one()
        line=self.issue_line_id
        picking_type = self.env.company.return_picking_id
        picking_pool = self.env['stock.picking']
        picking_id = picking_pool.create({
            'picking_type_id': picking_type.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'origin': f"Return:{line.issue_id.name}"
            })

        self.env['stock.move'].create({
            'product_id': line.book_id.id,
            'product_uom_qty': 1,
            'product_uom': line.book_id.uom_id.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
            'name': line.book_id.name,
            'picking_id': picking_id.id
        })
        picking_id.action_confirm()
        for move in picking_id.move_ids:
            move.quantity = move.product_uom_qty
        picking_id.button_validate()
        line.write({
            'return_date': self.return_date,
            'returned': True,
            'to_return': False
        })
        issue = line.issue_id
        remaining_books = issue.book_line_ids.filtered(lambda l: not l.returned)
        if remaining_books:
            issue.status = 'pending'
        else:
            issue.status = 'returned'
        return {
            'type': 'ir.actions.act_window_close'
        }


