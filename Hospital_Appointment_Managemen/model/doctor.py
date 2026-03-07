from odoo import fields,models

class doctor(models.Model):
    _name='hospital.doctor'
    _rec_name = 'name'

    name=fields.Char('Doctor_Name',required=True)
    specialization=fields.Char('Specialization',required=True)
    experience_years=fields.Char('Experience Years',required=True)
    is_available=fields.Boolean('Available')
    appointment_ids=fields.One2many('hospital.appointment','doctor_id',string='Appointments')
