from odoo import fields,models

class Task(models.Model):
    _name='my.tasks'
    _rec_name='name'

    name=fields.Char('Name')
    project_id = fields.Many2one('my.project', string='Project')
    priority=fields.Selection([('Low','Low'),('High','High'),('Medium','Medium')],Defalt='Medium',string='Priority')
    estimated_hours=fields.Float('Estimated Hours')
    status=fields.Selection([('New','New'),('In_progress','In_progress'),('Done','Done')],string='Status')
    project_member_ids=fields.Many2many('res.users',related='project_id.member_ids',string='Members')
    assignee_to = fields.Many2one('res.users', 'Assignee')
