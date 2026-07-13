from odoo import models, fields, tools

class HrAttendanceLateReport(models.Model):
    _name = "hr.attendance.late.report"
    _description = "Late Check-in Report"
    _auto = False
    _order = "check_in desc"

    employee_id = fields.Many2one("hr.employee","Employee",readonly=True)
    department_id = fields.Many2one("hr.department","Department",readonly=True)
    company_id = fields.Many2one("res.company","Company",readonly=True)
    check_in = fields.Datetime("Check-in Date",readonly=True)
    check_in_time = fields.Char("Check-in Time",readonly=True)
    late_minutes = fields.Integer("Late Minutes",readonly=True)
    attendance_id = fields.Many2one("hr.attendance","Attendance Reference",readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr,self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS
            (
                SELECT
                    ha.id AS id,
                    ha.id AS attendance_id,
                    ha.employee_id,
                    he.department_id,
                    he.company_id,
                    ha.check_in,
                    to_char(
                    ha.check_in AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata','HH24:MI:SS') AS check_in_time,
                    ha.late_minutes
                FROM hr_attendance ha
                JOIN hr_employee he
                    ON he.id = ha.employee_id
                WHERE ha.is_late = TRUE
            )
        """ % self._table)