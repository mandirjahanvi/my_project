from odoo import fields, models, api

class Exam(models.Model):
    _name = 'exam.schedule'
    _rec_name = 'name'

    name=fields.Char("Exam Name")
    class_id=fields.Many2one('education.class',string="Class")
    subject_id=fields.Many2one('education.subject',string="Subject")
    exam_date=fields.Date("Exam Date")
    start_time=fields.Datetime("Start Time")
    end_time=fields.Datetime("End Time")
    room_number=fields.Char("Room Number")
    teacher_id=fields.Many2one('edu.teacher',string="Supervisor")

class Marks(models.Model):
    _name='exam.marks'
    _rec_name = 'student_id'

    student_id=fields.Many2one('student.register',string='Student')
    exam_id=fields.Many2one('exam.schedule',string='Exam')
    subject_id=fields.Many2one('education.subject',string="Subject")
    marks_obtained=fields.Float("Marks Obtained")
    total_marks=fields.Float("Total Marks")
    percentage=fields.Float("Percentage",compute="_compute_percentage")
    grade=fields.Float("Grade")

    @api.depends('marks_obtained','total_marks')
    def _compute_percentage(self):
        for i in self:
            if i.total_marks:
                i.percentage =(i.mark_obtained / i.total_marks) * 100


class Grade(models.Model):
    _name='exam.grade'

    name=fields.Char("Grade Name")
    min_marks=fields.Float("Min Marks")
    max_marks=fields.Float("Max Marks")
    grade_point=fields.Float("Grade Point")
    description=fields.Text("Description")

class Result(models.Model):
    _name='exam.result'

    student_id=fields.Many2one('student.register',string='Student')
    exam_id=fields.Many2one('exam.schedule',string='Exam')
    total_marks=fields.Float("Total Marks")
    percentage=fields.Float("Percentage")
    grade=fields.Char("Grade")
    result_status=fields.Selection([('pass','Pass'),('fail','Fail')],string="Result")
    publish_date=fields.Date("Publish Date")

class Report(models.Model):
    _name='exam.report'

    student_id = fields.Many2one('student.register', string='Student')
    exam_id = fields.Many2one('exam.schedule', string='Exam')
    class_id=fields.Many2one('education.class',string="Class")
    subject_id=fields.Many2one('education.subject',string="Subjects")
    total_marks=fields.Float("Total Marks")
    percentage = fields.Float("Percentage")
    grade = fields.Float("Grade")
    rank=fields.Integer("Rank")
    pdf_file=fields.Binary("PDF Report Card")


