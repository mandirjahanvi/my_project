from odoo import models, fields,api

class student_register(models.Model):
    _name = 'student.register'
    _rec_name = 'name'

    name=fields.Char("Name")
    admission_no=fields.Char("Admission Number",required=True,readonly=True,copy=False,default='New')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    dob= fields.Date('Date of Birth')
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    photo=fields.Binary('Photo')
    active = fields.Boolean(default=True)
    document_ids=fields.One2many('student.document','student_id',string="Documents")
    zipcode = fields.Char()
    address = fields.Char('Address')
    city=fields.Char()
    country_id = fields.Many2one('res.country',required=True)
    state_id = fields.Many2one('res.country.state',domain="[('country_id', '=', country_id)]")

    @api.model
    def create(self, vals):
        if vals.get('admission_no', 'New') == 'New':
            vals['admission_no'] = self.env['ir.sequence'].next_by_code(
                'student.admission.sequence'
            ) or 'New'
        return super(student_register, self).create(vals)

class student_document(models.Model):
    _name = 'student.document'

    student_id=fields.Many2one('student.register',string='Student')
    document_type = fields.Selection([
        ('aadhar', 'Aadhar Card'),
        ('pan', 'PAN Card'),
        ('passport', 'Passport'),
        ('other', 'Other')
    ], string="Document Type", required=True)
    document_file = fields.Binary('Document File')
    file_name = fields.Char('File Name')
    class_id = fields.Many2one('education.class', string="Class")

