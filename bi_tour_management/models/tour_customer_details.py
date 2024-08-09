# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields

class tour_customer_details(models.Model):

    _name = "tour.customer.details"
    _description = "Tour Customer Details"

    trans_book_id = fields.Many2one('transport.booking', "Transport Booking Id")
    book_id = fields.Many2one('tour.booking', "Booking Id")
    cancel_id = fields.Many2one('tour.cancellation', "Cancel Id")
    hotel_book_id = fields.Many2one('tour.hotel.reservation', "Hotel Booking Id")
    partner_id = fields.Many2one('res.partner', 'Person', required=True)
    name = fields.Char('Age', required=True)
    room_no = fields.Char('Room Number')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], 'Gender', default="male")
    type = fields.Selection([
        ('adult', 'Adult'),
        ('child', 'Child')], "Type", default="adult", required=True)
    h_flag = fields.Boolean('H', readonly=True)
    t_flag = fields.Boolean('T', readonly=True)
    i_flag = fields.Boolean('I', readonly=False)
    v_flag = fields.Boolean('V', readonly=True)
    p_flag = fields.Boolean('P', readonly=False)
    state = fields.Selection([
        ('confirm', 'Confirm'),
        ('cancel', 'Cancel')], "States", readonly=True, default="confirm")
    company_id = fields.Many2one(
        related='trans_book_id.company_id',
        store=True, index=True, precompute=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: