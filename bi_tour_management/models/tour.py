# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api
import datetime
import random
from datetime import timedelta
    
class tour(models.Model):
    _name = "tour"
    _description = "Tour"

    name = fields.Char("Name")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def first_date_of_month(self, year, month):
        date = datetime.datetime(year, month, 1)
        return date.strftime("%Y-%m-%d")
    
    def last_day_of_month(self, year, month):
        if month == 12:
            date = datetime.datetime(year, month, 31)
        else:
            date = datetime.datetime(year, month + 1, 1) + timedelta(days=-1)
        return date.strftime("%Y-%m-%d")

    @api.model
    def get_data(self):
        total_draft_inquiry = 0
        total_confirmed_inquiary = 0
        total_tour_booking = 0
        total_tour_inprogress_booking = 0
        total_bookings_of_month = 0 
        total_bookings_of_week = 0 
        inquiry = self.env['tour.preference'].sudo().search([])
        booking = self.env['tour.booking'].sudo().search([])
        current_date = datetime.datetime.today().date()
        start_of_week = current_date - timedelta(days = current_date.weekday())
        end_of_week = current_date + timedelta(days = 6)
        first_date_of_month = self.first_date_of_month(current_date.year, current_date.month)
        last_date_of_month = self.last_day_of_month(current_date.year, current_date.month)
        if inquiry:
            total_draft_inquiry = len(
                inquiry.filtered(lambda l: l.state == 'draft'))
            total_confirmed_inquiary = len(
                inquiry.filtered(lambda l: l.state == 'confirm'))
        if booking:
            total_tour_booking = len(
                booking.filtered(lambda l: l.state == 'confirm'))
            total_tour_inprogress_booking = len(
                booking.filtered(lambda l: l.state == 'in_process'))
            total_bookings_of_week = self.env['tour.booking'].sudo().search_count([('current_date', '>=', start_of_week), ('current_date', '<=', end_of_week)])
            total_bookings_of_month = self.env['tour.booking'].sudo().search_count([('current_date', '>=', first_date_of_month), ('current_date', '<=', last_date_of_month)])
        return {'total_tour_booking': total_tour_booking, 'total_draft_inquiry': total_draft_inquiry, 'total_confirmed_inquiary': total_confirmed_inquiary, 'total_tour_inprogress_booking': total_tour_inprogress_booking, 'total_bookings_of_week': total_bookings_of_week, 'total_bookings_of_month': total_bookings_of_month}

    def generate_random_color(self):
        random_color = random.randint(0, 0xFFFFFF)
        hex_color = hex(random_color)[2:]
        hex_color = hex_color.rjust(6, '0')
        return '#' + hex_color

    @api.model
    def action_get_weekly_booking(self):
        current_date = datetime.datetime.today().date()
        start_of_week = current_date - timedelta(days = current_date.weekday())
        week_booking = []
        week_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        color_data = []
        for i in range(7):
            color = self.generate_random_color()
            color_data.append(color)
            search_date = start_of_week + timedelta(days = i)
            booking = self.env['tour.booking'].sudo().search_count([('current_date', '=', search_date)])
            week_booking.append(booking)
        return [week_booking, week_day, color_data]

    @api.model
    def action_get_monthly_booking(self):
        month_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        color_data = []
        current_date = datetime.datetime.today().date()
        month_booking = []
        booking = self.env['tour.booking'].sudo().search([])
        for i in range(1, 13):
            color = self.generate_random_color()
            color_data.append(color)
            first_date_of_month = self.first_date_of_month(current_date.year, i)
            last_date_of_month = self.last_day_of_month(current_date.year, i)
            booking = self.env['tour.booking'].sudo().search_count([('current_date', '>=', first_date_of_month), ('current_date', '<=', last_date_of_month)])
            month_booking.append(booking)
        return [month_booking, month_year, color_data]
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: