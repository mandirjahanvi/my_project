from odoo import models, fields, api
from odoo.exceptions import UserError


class PenaltyRange(models.Model):
    _name = 'penalty.range'
    _rec_name = 'from_day'

    from_day = fields.Integer("FROM DAY")
    to_day = fields.Integer("TO DAY")
    penalty_range = fields.Float("Extra penalty Charge(%)")
    company_id = fields.Many2one('res.company',"Company")

    @api.constrains('from_day','to_day','company_id')
    def check_range_overlapping(self):
        for rec in self:
            if rec.from_day >= rec.to_day:
                raise UserError("from day not greater or equal to to Days")
            records=self.search([('id', '!=',rec.id), ('company_id', '=', rec.company_id.id)])
            lapping=records.filtered(lambda r:rec.from_day <= r.to_days and rec.to_days >= r.from_day)
            if lapping:
            # for r in records:
            #     if rec.from_day <= r.to_day and rec.to_day >= r.from_day:
                    raise UserError("Range Overlapping... You can not do such things")

    # def create(self,vals):
    #     res_ids=super(PenaltyRange,self).create(vals)
    #     existing_recs = self.search([('id', 'not in', res_ids.ids),('company_id', '=', res_ids.company_id.id)])
    #     for res_id in res_ids:
    #         for rec in existing_recs:
    #             if rec.from_day <= res_id.to_day and rec.to_day >= res_id.from_day:
    #                 raise UserError("Range Overlapping... You can not do such things")
    #     return res_ids
    # def write(self,vals):
    #     res_id =super(PenaltyRange,self).write(vals)
    #     for rec in res_id:
    #         existing_recs = self.search([('id', 'not in', res_id.ids), ('company_id', '=', res_id.company_id.id)])
    #         for record in existing_recs:
    #             if record.from_day <= rec.to_day and record.to_day >= rec.from_day:
    #                 raise UserError("Range Overlapping... You can not do such things")
    #     return res_id


