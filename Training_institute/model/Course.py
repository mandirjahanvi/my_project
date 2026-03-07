from odoo import fields,models

class Course(models.Model):
    _name = 'training.course'
    _rec_name = 'name'

    name=fields.Selection([('android app development','Android App Development'),
                                  ('flutter app development','Flutter App Development'),
                                  ('graphic design','Graphic Design'), ('ui/ux','UI/UX'),
                                 ('web development(php with laravel)','Web Development(PHP WITH LARAVEL)'),
                                 ('web development(mern stack)','Web Development(MERN STACK)'),
                                 ('advance python with Odoo','Advance Python with Odoo'),
                                 ('Advanced 3D Animation with AI','advanced 3d animation with ai'),
                                 ('seo','SEO'),
                                 ('digital marketing','Digital Marketing'),('tally','Tally'),
                                 ('power bi','Power BI'), ('ccc', 'CCC')], string="Course Name")
    fees=fields.Float("Fees")
    duration_days=fields.Char("Duration Days")
    is_active = fields.Boolean("Is Active",default=True)
    level=fields.Selection([('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced')],string='level')
    batch_ids = fields.One2many('training.batch', 'course_id', string='Batches')
    student_ids=fields.Many2many('training.student',string='Students')
