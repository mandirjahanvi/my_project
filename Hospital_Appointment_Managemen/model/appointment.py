from odoo import fields,models

class appointment(models.Model):
    _name='hospital.appointment'
    _rec_name = 'patient_id'

    patient_id=fields.Many2one('hospital.patient',string='Patient')
    doctor_id=fields.Many2one('hospital.doctor',string='Doctor',domain=[('is_available', '=', True)])
    appointment_date=fields.Datetime(string='Appointment Date')
    fees=fields.Integer(string='Fees')
    status = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')])
    is_paid = fields.Boolean('Paid', default=False)