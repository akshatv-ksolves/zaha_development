# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class tour_dates(models.Model):

    _name = "tour.dates"
    _description = "Tour Dates"
    _rec_name="start_date"
    

    tour_id = fields.Many2one('tour.package', 'Package')
    season_id=fields.Many2one('tour.season','Season', required=True)
    start_date = fields.Date('Start Date', required=True)
    book_date = fields.Date('Last Date Of Booking', required=True)
    due_date = fields.Date('Payment Due Date', required=True)
    total_seat = fields.Integer('Total Seats')
    available_date = fields.Integer('Available Seats')
    state = fields.Selection([('draft','Draft'),
                              ('available','Available'),
                              ('closed','Closed'),
                              ('reopen','Reopen')],readonly=True,default="draft",string="Status")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def change_state(self):
        for rec in self:
            if rec.due_date < rec.start_date:
                identifier = rec.state
                if identifier == 'draft':
                    rec.state = 'available'
                if identifier == 'available':
                    rec.state = 'closed'
                if identifier == 'closed':
                    rec.state = 'draft'
            else:
                raise UserError('Payment Due Date  is Greater then Start Date ')
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        