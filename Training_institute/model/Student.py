from odoo import models, fields

class Training(models.Model):
    _name='training.student'
    _rec_name = 'name'

    name=fields.Char('Name')
    email=fields.Char('Email')
    phone=fields.Char('Phone')
    age=fields.Integer('Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    course_id=fields.Many2many('training.course',string='Courses')
    batch_ids =fields.Many2one('training.batch',string='Batch',domain="[('course_id','in',course_id)]")