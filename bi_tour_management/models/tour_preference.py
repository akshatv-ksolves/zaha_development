# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class tour_preference(models.Model):

    _name = "tour.preference"
    _description = "Tour Preference"

    name = fields.Char("Inquiry No. ",readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('cancel', 'Cancelled'),
        ],string="status",default="draft", readonly=True)
    current_date = fields.Date('Inquiry Date',required=True)
    lead_id = fields.Many2one('crm.lead','Lead',readonly=True)
    contact_name = fields.Char("Contact Name ")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Origin')
    
    email_id = fields.Char("Email Id")
    mobile = fields.Char("Mobile Number", required=True)
    adult = fields.Integer("Adult Persons")
    child = fields.Integer("Child")
    checkin_date = fields.Date('Prefer Start Date',required=True)
    checkout_date = fields.Date('Prefer End Date',required=True)
    tour_low_price = fields.Float("Budget/ Person (min/max)")
    tour_high_price = fields.Float("Max Budget")
    destination_lines_ids = fields.One2many('custom.tour.destination','tour_preference_id','Destination Preferences')
    hotel_type_id = fields.Many2one('hotel.type','Hotel Type')
    room_type_id = fields.Many2one('room.type','Room Type')
    room_req = fields.Integer('No of Room Required')
    low_price = fields.Integer('Price Limit (min/max)')
    high_price = fields.Integer('')
    transport_ids = fields.One2many('custom.tour.transport','tour_preference_id','Transport Preferences')
    via= fields.Selection([
        ('direct', 'Direct'),
        ('agent', 'Agent'),
        ],string="Via",default="direct")
    agent_id = fields.Many2one('res.partner','Agent')


    @api.constrains('checkin_date')
    def check_checkin_date(self):
        for rec in self:
            if rec.checkin_date > rec.checkout_date:
                raise ValidationError("Prefer Start Date Can not Greater than Prefer End Date.")

    @api.constrains('checkout_date')
    def check_checkout_date(self):
        for rec in self:
            if rec.checkout_date < rec.checkin_date:
                raise ValidationError("Prefer End Date Can not Greater than Prefer Start Date.")

    def btn_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get('tour.preference') or '/'
        res = super(tour_preference, self).create(vals)
        return res
    
    @api.onchange('lead_id')
    def onchange_lead(self):
        for rec in self:
            if rec.lead_id.partner_id or rec.lead_id.partner_name:
                rec.contact_name = rec.lead_id.partner_id.name or rec.lead_id.partner_name or False
                rec.mobile = rec.lead_id.partner_id.mobile or rec.lead_id.phone or rec.lead_id.mobile or False
                rec.email_id = rec.lead_id.partner_id.email or rec.lead_id.email_from or False
                rec.street = rec.lead_id.street or False
                rec.street2 = rec.lead_id.street2 or False
                rec.zip = rec.lead_id.zip or False
                rec.city = rec.lead_id.city or False
                rec.state_id = rec.lead_id.state_id or False
                rec.country_id = rec.lead_id.country_id or rec.lead_id.country_id.id or False
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 