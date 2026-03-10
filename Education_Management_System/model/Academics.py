from odoo import fields,models,api

class EducationClass(models.Model):
    _name = "education.class"
    _rec_name = 'class_Name'

    class_Name=fields.Char("Name")
    code=fields.Char("Code")
    class_Teacher=fields.Many2one('edu.teacher',string="Teacher")
    academic_year=fields.Many2one('edu.year',string="Academic Year")
    section = fields.Selection([('a', 'A'),('b', 'B'),('c', 'C') ],string="Section")
    capacity=fields.Integer("Capacity")
    description=fields.Text("Description")
    active=fields.Boolean("Active",default=True)
    subject_id = fields.Many2one('education.subject', string="Subject")

class Academic_year(models.Model):
    _name='edu.year'
    _rec_name = 'name'

    name = fields.Char("Academic Year")

class Timetable(models.Model):
    _name="edu.timetable"
    _rec_name ='subject_id'

    subject_id=fields.Many2one('education.subject',string="Subject")
    teacher_id=fields.Many2one('edu.teacher',string="Teacher")
    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")

class Subject(models.Model):
    _name = "education.subject"

    name=fields.Char("Subject")
    code=fields.Char("Code")
    class_id=fields.Many2one('education.class',string="Class")
    teacher_id=fields.Many2one('edu.teacher',string="Teacher")

    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id and self.class_id.class_Teacher:
            self.teacher_id = self.class_id.class_Teacher
        else:
            self.teacher_id = False




