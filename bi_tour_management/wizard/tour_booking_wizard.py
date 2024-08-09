# -*- coding: utf-8 -*-
#####
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
#####
from odoo import api, fields, models, _


class TourBookingWizard(models.TransientModel):
    _name = "tour.booking.wizard"

    res_partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    mobile_number = fields.Char(string="Mobile Number", required=True)
    email = fields.Char(string="Email Id", required=True)
    res_currency_id = fields.Many2one("res.currency", string="Currency", required=True)
    select_tour_type = fields.Selection([
        ('international', 'International'),
        ('domastic', 'Domastic')],
        string="Tour Type", required=True)
    tour_season_id = fields.Many2one("tour.season", string="Season", required=True)
    tour_dates_id = fields.Many2one("tour.dates", string="Tour Dates", required=True)
    tour_payment_policy_id = fields.Many2one("tour.payment.policy", string="Payment Policy", required=True)
    tour_package_id = fields.Many2one("tour.package", string="Tour", required=True)

    def button_tour_book_wizard(self):
        for record in self:
            tour_booking_ids = self.env["tour.booking"].create({
                'customer_id': record.res_partner_id.id,
                'mobile1': record.mobile_number,
                'email_id': record.email,
                'pricelist_id': record.res_currency_id.id,
                'tour_type': record.select_tour_type,
                'season_id': record.tour_season_id.id,
                'tour_dates_id': record.tour_dates_id.id,
                'payment_policy_id': record.tour_payment_policy_id.id,
                'tour_id': record.tour_package_id.id,
            })
        return {
            'view_mode': 'form',
            'res_model': 'tour.booking',
            'res_id': tour_booking_ids.id,
            'view_type': 'form',
            'type': 'ir.actions.act_window',
        }
