from odoo import models, fields,api


class EducationCourse(models.Model):
    _name = "education.course"
    _description = "Course"
    _rec_name = "name"

    name = fields.Char("Course Name", required=True)
    duration = fields.Char("Duration")
    total_semester = fields.Integer("Total Semesters")
    semester_id=fields.One2many('education.semester','course_id',string="Semester")
    active = fields.Boolean("Active", default=True)

    def action_open_semester(self):
        index = self.env.context.get('semester_index', 0)
        semesters = self.semester_id.sorted('sequence')

        if index >= len(semesters):
            return

        semester = semesters[index]

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'education.semester',
            'view_mode': 'form',
            'res_id': semester.id,
        }
    @api.model
    def create(self, vals):
        record = super().create(vals)

        total = record.total_semester or 0

        for i in range(1, total + 1):
            self.env['education.semester'].create({
                'name': f"Semester {i}",
                'sequence': i,
                'course_id': record.id,
            })

        return record

    def write(self, vals):
        res = super().write(vals)

        if 'total_semester' in vals:
            for rec in self:
                existing = len(rec.semester_id)
                total = rec.total_semester

                if total > existing:
                    for i in range(existing + 1, total + 1):
                        self.env['education.semester'].create({
                            'name': f"Semester {i}",
                            'sequence': i,
                            'course_id': rec.id,
                        })

        return res

class Academic_year(models.Model):
    _name='edu.year'
    _rec_name = 'name'

    name = fields.Char("Academic Year")

class Semester(models.Model):
    _name="education.semester"
    _rec_name = 'name'
    _order = "sequence"

    name = fields.Char("Semester")
    sequence = fields.Integer("Sequence")
    course_id=fields.Many2one('education.course',string="Course",required=True)
    subject_id = fields.One2many('education.subject', 'semester_id', string="Subjects")
    syllabus_pdf=fields.Binary('Syllabus PDF')
    syllabus_filename = fields.Char("File Name")

class Subject(models.Model):
    _name = "education.subject"

    name = fields.Char("Subject Name",required=True)
    subject_code=fields.Char("Subject Code")
    semester_id=fields.Many2one('education.semester',string="Semester",required=True)
    unit_ids=fields.One2many('education.unit','subject_id',string="Units")

class Unit(models.Model):
    _name = "education.unit"
    _rec_name = "name"

    name = fields.Char("Unit Name")
    subject_id = fields.Many2one('education.subject',string="Subject")

class Timetable(models.Model):
    _name="edu.timetable"
    _rec_name ='subject_id'

    subject_id=fields.Many2one('education.subject',string="Subject")
    teacher_id=fields.Many2one('edu.teacher',string="Teacher")
    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")

def action_open_semesters(self):
    return {
        'type': 'ir.actions.act_window',
        'name': 'Semesters',
        'res_model': 'education.semester',
        'view_mode': 'kanban,list,form',
        'domain': [('course_id', '=', self.id)],
        'context': {'default_course_id': self.id},
    }



