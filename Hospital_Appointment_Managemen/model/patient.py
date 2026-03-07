from odoo import fields,models

class patient(models.Model):
    _name='hospital.patient'
    _rec_name = 'name'

    name=fields.Char('Patient_name',required=True)
    age=fields.Char('Age',required=True)
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')
    blood_group=fields.Selection([('o+','O+'),('o-','O-'),('a+','A+'),('a-','A-'),('b+','B+'),('b-','B-'),('ab-','AB-'),('ab+','AB+')],string='Blood Group')
    appointment_ids=fields.One2many('hospital.appointment','doctor_id',string='Appointments')