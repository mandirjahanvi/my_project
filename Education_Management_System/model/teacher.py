from odoo import models, fields

class Teacher(models.Model):
    _name = 'edu.teacher'
    _rec_name = 'name'

    name=fields.Char('Name')
    dob=fields.Date('Date of Birth')
    email=fields.Char('Email')
    phone=fields.Char('Phone Number')
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')
    qualification=fields.Selection([('graduate','Graduate'),('post graduate','Post Graduate'),('phd','PHD'),('other','Other')],string='Qualification')
    experience=fields.Integer('Experience')
    joining_date=fields.Date('Joining Date')
    basic_salary=fields.Float('Basic Salary')
    photo=fields.Binary('Photo')
    teacher_id=fields.Many2one('education.class',string='Teacher')


