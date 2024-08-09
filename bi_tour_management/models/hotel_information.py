# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################

from odoo import models, fields, api, _

class hotel_information(models.Model):

    _name = "hotel.information"
    _description = "Hotel Information"

    name = fields.Char('Name', related= 'hotel_partner_id.name',readonly=True)
    hotel_type_id = fields.Many2one('hotel.type','Hotel Type',required=True)
    hotel_partner_id  = fields.Many2one('res.partner','Hotel ',required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm')],
        string="Status",default="draft")
    room_info_ids = fields.One2many('room.info','hotel_information_id','Room Information')
    hotel_service_ids = fields.One2many('hotel.service','hotel_information_id','service Information')
    rcv_account_id = fields.Many2one('account.account','Receivable Account',required=True)
    pay_account_id = fields.Many2one('account.account','Payable Account',required=True)
    hotel_img1 = fields.Binary('Image1')
    hotel_img2 = fields.Binary('Image2')
    hotel_img3 = fields.Binary('Image3')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def confirm_info(self):
        for rec in self:
            rec.state = 'confirm'

   
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: