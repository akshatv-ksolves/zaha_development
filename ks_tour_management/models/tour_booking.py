from odoo import models, fields, api

class TourBooking(models.Model):
    _inherit = 'tour.booking'

    booking_mail = fields.Boolean(string='Confirmation Mail Sent',track_visibility='onchange')

    def trip_confirm_mail_action(self):
        self.ensure_one()
        template = self.env.ref('ks_tour_management.tour_confirm_mail_template')
        # template = self.env.ref('ks_tour_management.tour_quotation_mail_template')
        # template = self.env.ref('ks_tour_management.follow_up_mail_template')
        # template = self.env.ref('ks_tour_management.customer_feedback_mail_template')
        # template = self.env.ref('ks_tour_management.payment_done_mail_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)

    @api.model
    def create(self, vals):
        record = super(TourBooking, self).create(vals)
        if record.state == 'in_process':
            record.trip_confirm_mail_action()
        return record

    def write(self, vals):
        res = super(TourBooking, self).write(vals)
        for record in self:
            if 'state' in vals and record.state == 'in_process' and not record.booking_mail:
                record.trip_confirm_mail_action()
                record.booking_mail = True
        return res

    def book_hotel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'new.student',
            'view_mode': 'form',
            'view_id': self.env.ref('om_school.view_school_student_form').id,
            'res_model': 'school.student',
            'context': {},
        }