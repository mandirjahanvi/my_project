from odoo import models,fields,api

class Exam(models.Model):
    _name = 'exam.schedule'
    _rec_name = 'name'

    name=fields.Char("Exam Name")
    class_id=fields.Many2one('education.course',string="Class")
    subject_id=fields.Many2one('education.subject',string="Subject")
    exam_date=fields.Date("Exam Date")
    start_time=fields.Datetime("Start Time")
    end_time=fields.Datetime("End Time")
    room_number=fields.Char("Room Number")
    teacher_id=fields.Many2one('edu.teacher',string="Supervisor")

class Grade(models.Model):
    _name='exam.grade'

    name=fields.Char("Grade Name")
    min_marks=fields.Float("Min Marks")
    max_marks=fields.Float("Max Marks")
    grade_point=fields.Float("Grade Point")
    description=fields.Text("Description")

class Result(models.Model):
    _name='exam.result'
    _description = 'Student Result'

    student_id=fields.Many2one('student.register',string='Student',required=True)
    exam_id=fields.Many2one('exam.schedule',string='Exam',required=True)
    total_obtained =fields.Float("Total Obtained",compute="compute_result",store=True)
    total_marks =fields.Float("Total Marks",compute="compute_result",store=True)
    result_line=fields.One2many('student.result.line','result_id','Subjects')
    percentage=fields.Float("Percentage",compute="compute_result",store=True)
    grade=fields.Char("Grade",compute="compute_result",store=True)
    result_status=fields.Selection([('pass','Pass'),('fail','Fail')],string="Result_status",compute="compute_result",store=True)

    @api.depends('result_line.marks_obtained', 'result_line.total_marks')
    def compute_result(self):
        for i in self:
            obtained = sum(line.marks_obtained for line in i.result_line)
            total = sum(line.total_marks for line in i.result_line)
            i.total_obtained = obtained
            i.total_marks = total

            if total > 0:
                percentage = (obtained / total) * 100
            else:
                percentage = 0.0

            i.percentage = percentage

            grade = self.env['exam.grade'].search([
                ('min_marks', '<=', percentage),
                ('max_marks', '>=', percentage)
            ], limit=1)

            i.grade = grade.name if grade else ''

            if percentage >= 40:
                i.result_status = 'pass'
            else:
                i.result_status = 'fail'



class Result_Line(models.Model):
    _name='student.result.line'

    result_id=fields.Many2one('exam.result',string='Result')
    subject_id=fields.Many2one('education.subject',string="Subjects",required=True)
    marks_obtained=fields.Float("Marks Obtained")
    total_marks=fields.Float("Total Marks")


class Report(models.Model):
    _name='exam.report'
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.register', string='Student')
    exam_id = fields.Many2one('exam.schedule', string='Exam')
    class_id=fields.Many2one('education.class',string="Class")
    subject_id=fields.Many2one('education.subject',string="Subjects")
    total_marks=fields.Float("Total Marks")
    percentage = fields.Float("Percentage")
    grade = fields.Char("Grade")
    rank=fields.Integer("Rank")
    pdf_file=fields.Binary("PDF Report Card")


