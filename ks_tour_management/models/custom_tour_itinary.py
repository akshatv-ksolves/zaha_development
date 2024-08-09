from odoo import models, fields, api, _

class custom_tour_itinary(models.Model):
    _inherit = "custom.tour.itinary"


    def send_quotation_mail_action(self):
        self.ensure_one()
        template = self.env.ref('ks_tour_management.tour_quotation_mail_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)
