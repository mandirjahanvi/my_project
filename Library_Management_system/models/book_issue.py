from odoo import models, fields,api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class book_issue(models.Model):
    _name = 'book.issue'
    _rec_name = 'name'

    name=fields.Char('Reference',required=True,copy=False,readonly=True,default='New')
    book_line_ids = fields.One2many('book.issue.line','issue_id',string='Books')
    member_id = fields.Many2one('library.member', string="Member", required=True)
    status=fields.Selection([('draft','Draft'),('issued','Issued'),('pending','Pending'),('returned','Returned')],default='draft',string='Status',tracking=True)
    penalty=fields.Float("Penalty",compute="compute_penalty", store=True)
    picking_id = fields.Many2one('stock.picking')
    # invoice_id = fields.Many2one('account.move', string="Penalty Invoice")
    selected_book_ids = fields.Many2many('product.product',compute='compute_selected_books')
    member_photo = fields.Image(related='member_id.photo',string='Member Photo',store=True)
    payment_ids=fields.One2many('library.penalty.payment','issue_id',string="Payments")
    payment_count=fields.Integer(compute='_compute_payment_count')
    payment_state = fields.Selection([('unpaid', 'Unpaid'),('paid', 'Paid')],compute='_compute_payment_state',store=True)

    def action_open_issue_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Book Issue',
            'res_model': 'book.issue',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'book.issue.sequence'
            ) or 'New'
        return super().create(vals)

    @api.depends('book_line_ids.book_id')
    def compute_selected_books(self):
        for rec in self:
            rec.selected_book_ids = rec.book_line_ids.mapped('book_id')

    @api.depends('payment_ids.state', 'payment_ids.amount', 'penalty')
    def _compute_payment_state(self):
        for rec in self:
            if rec.penalty <= 0:
                rec.payment_state = 'unpaid'
                continue
            paid_amount = sum(rec.payment_ids.filtered(lambda p: p.state == 'paid').mapped('amount'))
            rec.payment_state = ('paid' if paid_amount >= rec.penalty else 'unpaid')

    @api.depends('payment_ids')
    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    def action_pay_penalty(self):
        self.ensure_one()
        paid_amount = sum(
            self.payment_ids.filtered(
                lambda p: p.state == 'paid'
            ).mapped('amount')
        )
        remaining = self.penalty - paid_amount
        if remaining <= 0:
            payment = self.payment_ids.filtered(lambda p: p.state == 'paid')[:1]
            return {
                'type': 'ir.actions.act_window',
                'name': 'Payment',
                'res_model': 'library.penalty.payment',
                'res_id': payment.id,
                'view_mode': 'form',
                'target': 'new',
            }
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pay Penalty',
            'res_model': 'library.penalty.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_issue_id': self.id,
                'default_amount': remaining,
            }
        }

    def action_view_payments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'library.penalty.payment',
            'view_mode': 'list,form',
            'domain': [('issue_id', '=', self.id)],
        }

    @api.depends('book_line_ids.penalty')
    def compute_penalty(self):
        for rec in self:
            rec.penalty = sum(rec.book_line_ids.mapped('penalty'))

    def action_issue_book(self):
        if not self.book_line_ids:
            raise UserError("Please add books.")
        picking_pool = self.env['stock.picking']
        picking_type = self.env.company.issue_picking_id
        picking_id = picking_pool.create({
               'picking_type_id': picking_type and picking_type.id or False,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
                'origin': f"Issue ID:{self.id}"
            })
        for line in self.book_line_ids:
            product = line.book_id
            move_id = self.env['stock.move'].create({
                'product_id': product.id,
                'product_uom_qty': 1,
                'product_uom': product.uom_id.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
                'name': product.name,
                'picking_id': picking_id.id
            })
        picking_id.action_confirm()
        picking_id.action_assign()
        if picking_id.state != 'assigned':
            raise UserError("Stock not available for all books")
        picking_id.button_validate()
        self.picking_id = picking_id.id
        today = fields.Date.today()
        validity_days = self.env.company.book_validity or 7
        for line in self.book_line_ids:
            line.issue_date = today
            line.last_date_of_return = today + timedelta(days=validity_days)
        self.status = 'issued'

    def action_return_book(self):
        picking_type = self.env.company.return_picking_id
        if not picking_type:
            raise UserError("Return Picking Type is not configured in Company")
        selected_lines = self.book_line_ids.filtered(lambda l: l.to_return and not l.returned)
        if not selected_lines:
            raise UserError("Please select at least one book to return.")
        picking_pool = self.env['stock.picking']
        picking_id = picking_pool.create({
                'picking_type_id': picking_type.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
                'origin': f"Return ID:{self.id}"})
        for line in selected_lines:
            if line.book_id.qty_available <= 0:
                raise UserError(f"Book '{line.book_id.name}' is out of stock.")
            move_id = self.env['stock.move'].create({
                    'product_id': line.book_id.id,
                    'product_uom_qty': 1,
                    'product_uom': line.book_id.uom_id.id,
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': picking_type.default_location_dest_id.id,
                    'name': 'Return Product Move',
                    'picking_id': picking_id.id
                })
        picking_id.action_confirm()
        if picking_id.state != 'assigned':
            raise UserError("Insufficient stock available.")
        for move in picking_id.move_ids:
            move.quantity = move.product_uom_qty
        picking_id.button_validate()
        for line in selected_lines:
            line.returned = True
            line.to_return = False
            line.return_date = fields.Date.today()
        self.status = 'returned' if all(self.book_line_ids.mapped('returned')) else 'pending'


class BookIssueLine(models.Model):
    _name = 'book.issue.line'

    issue_id = fields.Many2one('book.issue',string='Issue')
    book_id = fields.Many2one('product.product',string='Book',required=True)
    to_return = fields.Boolean(string="Return")
    returned = fields.Boolean(string='Returned',default=False)
    return_date=fields.Date('Return Date')
    issue_date = fields.Date('Issue Date', default=fields.Date.today)
    last_date_of_return = fields.Date("Due Date")
    days_issued = fields.Integer("Days",compute="_compute_book",store=True)
    penalty = fields.Float(string='Penalty',compute='compute_line_penalty',store=True)

    @api.depends('issue_date', 'return_date')
    def _compute_book(self):
        for book in self:
            if book.issue_date:
                end_date = book.return_date or fields.Date.today()
                book.days_issued = max((end_date - book.issue_date).days, 0)
            else:
                book.days_issued = 0

    @api.constrains('issue_id', 'book_id')
    def _check_duplicate_books(self):
        for rec in self:
            books = rec.issue_id.book_line_ids.mapped('book_id')
            if len(books) != len(set(books)):
                raise ValidationError("Same book cannot be selected twice in one issue.")

    @api.depends('return_date', 'last_date_of_return')
    def compute_line_penalty(self):
        company = self.env.company
        for book in self:
            book.penalty = 0
            if book.return_date and book.last_date_of_return and book.return_date > book.last_date_of_return:
                delay = book.return_date - book.last_date_of_return
                delay_days = max(delay.days, 0)
                penalty_amt = company.penalty_charge or 0
                record = self.env['penalty.range'].search([('from_day', '<=', delay_days), ('to_day', '>=', delay_days),
                                                           ('company_id', '=', self.env.company.id)], limit=1)
                penalty_percentage = record.penalty_range if record else 0
                book.penalty = penalty_amt + (penalty_amt * (penalty_percentage / 100))

    def action_update_return(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Update Return Date',
            'res_model': 'return.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_issue_line_id': self.id,
                'default_return_date': self.return_date
            }
        }
