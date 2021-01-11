# -*- coding: utf-8 -*-

from flectra import models, fields, api, _

# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()

class HospitalPatient(models.Model):

    @api.depends('patient_age')
    def set_age_group(self):
        for iteration in self:
            if iteration.patient_age:
                if iteration.patient_age < 18:
                    iteration.age_group =  'minor'
                else:
                    iteration.age_group = 'major'

    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Records'
    _rec_name = 'patient_name'

    patient_name = fields.Char(String='Name', required=True)
    patient_age = fields.Integer('Age')
    notes = fields.Text(String='Notes')
    image = fields.Binary(String='Image')
    name_seq = fields.Char(string='Patient Sequence', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    gender = fields.Selection([('male','Male'),('fe_male','Female')], default='male', string="Gender")
    age_group = fields.Selection([('major','Major'),('minor','Minor')], string="Age Group", compute='set_age_group')

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')

        result = super(HospitalPatient, self).create(vals)
        return result