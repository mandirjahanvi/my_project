import qrcode
import base64
from io import BytesIO
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string="Member Name", required=True, ondelete="cascade")
    member_code=fields.Char('Membership ID', required=True,copy=False,readonly=True,default='New')
    photo = fields.Image(string="Photo")
    gender = fields.Selection([('male', 'Male'),('female', 'Female'),('other', 'Other')],string='Gender')
    dob = fields.Date(string='Date of Birth')
    aadhar_number = fields.Char(string="Aadhar Number", required=True)
    mobile = fields.Char(string='Mobile Number')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    state = fields.Char(string='State')
    zip_code = fields.Char(string='ZIP Code')
    country_id = fields.Many2one('res.country',string='Country')
    membership_type = fields.Selection([('student', 'Student'),('teacher', 'Teacher'),('staff', 'Staff'),('general', 'General')], string='Membership Type')
    join_date = fields.Date(string='Joining Date', default=fields.Date.today)
    expiry_date = fields.Date(string='Membership Expiry',compute = 'membership_expire',store=True)
    penalty_due = fields.Float('Penalty Due',compute = 'compute_penalty')
    active = fields.Boolean(string = 'Active',default = True)
    notes = fields.Text(string='Notes')
    issue_ids = fields.One2many('book.issue','member_id',string='Book Issues')
    penalty_qr = fields.Binary(compute="_compute_penalty_qr")

    @api.constrains('aadhar_number')
    def _check_duplicate_aadhar(self):
        for rec in self:
            if rec.aadhar_number:
                existing = self.search([
                    ('aadhar_number', '=', rec.aadhar_number),
                    ('id', '!=', rec.id)
                ], limit=1)

                if existing:
                    raise ValidationError(
                        "A member with this Aadhaar Number already exists!"
                    )

    @api.depends('issue_ids.penalty')
    def compute_penalty(self):
        for rec in self:
            rec.penalty_due = sum(rec.issue_ids.mapped('penalty'))

    @api.model
    def create(self, vals):
        if vals.get('member_code', 'New') == 'New':
            vals['member_code'] = self.env['ir.sequence'].next_by_code( 'library.member.sequence') or 'New'
        return super().create(vals)

    def action_download_member_report(self):
        self.ensure_one()
        return self.env.ref(
            'library_management_system.action_report_member_history'
        ).report_action(self)

    @api.depends('join_date')
    def membership_expire(self):
        for rec in self:
            if rec.join_date:
                rec.expiry_date = rec.join_date + relativedelta(years=1)
            else:
                rec.expiry_date = False

    @api.depends('penalty_due')
    def _compute_penalty_qr(self):
        for rec in self:
            if rec.penalty_due <= 0:
                rec.penalty_qr = False
                continue
            qr = qrcode.make(
                f"Penalty Amount : ₹{rec.penalty_due}"
            )
            buffer = BytesIO()
            qr.save(buffer, format='PNG')
            rec.penalty_qr = base64.b64encode(
                buffer.getvalue()
            )

