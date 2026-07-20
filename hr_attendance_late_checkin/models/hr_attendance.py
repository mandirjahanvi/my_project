from odoo import models, fields, api
from datetime import time


class HR_Attendance(models.Model):
    _inherit = "hr.attendance"

    is_late = fields.Boolean("Late Check-in",compute="_compute_late_checkin",store=True)
    late_minutes = fields.Integer("Late Minutes",compute="_compute_late_checkin",store=True)

    @api.depends('check_in')
    def _compute_late_checkin(self):
        standard_time = time(10, 0)
        for rec in self:
            rec.is_late = False
            rec.late_minutes = 0
            if not rec.check_in:
                continue
            local_dt = fields.Datetime.context_timestamp(rec,rec.check_in,)
            late_minutes = ((local_dt.hour * 60 + local_dt.minute)- (10 * 60))
            if late_minutes > 0:
                rec.is_late = True
                rec.late_minutes = late_minutes
