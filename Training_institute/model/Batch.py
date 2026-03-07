from odoo import fields,models

class Batch(models.Model):
    _name='training.batch'
    _rec_name = 'name'

    name=fields.Char('Name',required=1)
    course_id=fields.Many2one('training.course',string='Course',domain=[('is_active', '=', True)])
    start_date=fields.Date('Start Date')
    end_date=fields.Date('End Date')
    capacity=fields.Integer('Capacity')
    student_ids=fields.One2many('training.student','batch_ids',string='Students')