from odoo import models,fields,api

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
    percentage=fields.Float("Percentage",compute="_compute_percentage",store=True)
    grade_id = fields.Many2one('exam.grade', string="Grade", compute="_compute_percentage", store=True)

    @api.depends('marks_obtained', 'total_marks')
    def _compute_percentage(self):
        for i in self:

            if i.total_marks:
                percentage = (i.marks_obtained / i.total_marks) * 100
            else:
                percentage = 0.0

            i.percentage = percentage
            grade=self.env['exam.grade'].search([ ('min_marks', '<=', percentage),('max_marks', '>=', percentage)],limit=1)
            i.grade_id =grade.id


class Grade(models.Model):
    _name='exam.grade'

    name=fields.Char("Grade Name")
    min_marks=fields.Float("Min Marks")
    max_marks=fields.Float("Max Marks")
    grade_point=fields.Float("Grade Point")
    description=fields.Text("Description")

class Result(models.Model):
    _name='exam.result'
    _rec_name = 'student_id'

    student_id=fields.Many2one('student.register',string='Student')
    exam_id=fields.Many2one('exam.schedule',string='Exam')
    total_marks=fields.Float("Total Marks",compute="compute_result")
    percentage=fields.Float("Percentage",compute="compute_result")
    grade=fields.Char("Grade",compute="compute_result")
    result_status=fields.Selection([('pass','Pass'),('fail','Fail')],string="Result")
    publish_date=fields.Date("Publish Date")

    @api.depends('student_id')
    def compute_result(self):
        for i in self:
            marks = self.env['exam.marks'].search([('student_id', '=', i.student_id.id),('exam_id', '=', i.exam_id.id)])
            total = sum(marks.mapped('marks_obtained'))
            total_max = sum(marks.mapped('total_marks'))

            if total_max:
                percentage = (total / total_max) * 100
            else:
                percentage = 0
            i.total_marks = total
            i.percentage = percentage
            if percentage >= 90:
                i.grade = 'A'
            elif percentage >= 80:
                i.grade = 'B'
            elif percentage >= 70:
                i.grade = 'C'
            elif percentage >= 60:
                i.grade = 'D'
            else:
                i.grade = 'F'

class Report(models.Model):
    _name='exam.report'
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.register', string='Student')
    exam_id = fields.Many2one('exam.schedule', string='Exam')
    class_id=fields.Many2one('education.class',string="Class")
    subject_id=fields.Many2one('education.subject',string="Subjects")
    total_marks=fields.Float("Total Marks")
    percentage = fields.Float("Percentage")
    grade = fields.Float("Grade")
    rank=fields.Integer("Rank")
    pdf_file=fields.Binary("PDF Report Card")


