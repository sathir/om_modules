# -*- coding: utf-8 -*-

from flectra.tools.func import default
from flectra import models, fields, api, _

# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = "appointment_date desc"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        
        result = super(HospitalAppointment, self).create(vals)
        return result

    def _get_default_note(self):
        return "Patient got an normal appointment"

    name = fields.Char(string='Appointent_ID', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note", default=_get_default_note)
    appointment_date = fields.Date(string='Date', required=True)
