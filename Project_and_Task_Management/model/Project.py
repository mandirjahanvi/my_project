from odoo import fields,models

class Project(models.Model):
    _name='my.project'
    _rec_name = 'name'
#sadsadas
    name=fields.Char('Name')
    customer_id=fields.Integer('Customer ID')
    budget=fields.Float('Budget')
    is_active=fields.Boolean('Is Active')
    task_ids=fields.One2many('my.tasks','project_id',string='Tasks')
    member_ids=fields.Many2many('res.users','my_project_user_rel','member_ids','user_id',string='Members')
