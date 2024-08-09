# -*- coding: utf-8 -*-
################################################################################
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
################################################################################
from odoo import models, fields, api, _

class tour_cancellation(models.Model):
    
    _name = "tour.cancellation"
    _description = "Tour Cancellation"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In Process'),
        ('done', 'Done'),
        ],string="Status", default="draft",readonly=True)
    tour = fields.Many2one('tour.booking','Tour Booking ID')
    cancel_date =fields.Date("Tour Cancel Date" , default=fields.date.today().strftime('%Y-%m-%d'), required=True)
    name = fields.Char("Tour Cancellation ID" )
    current_date =fields.Date("Booking Date" ,required=True )
    customer_id = fields.Many2one('res.partner',)
    email_id = fields.Char("Email Id" ,)
    mobile1 = fields.Char("Mobile Number" ,)
    adult = fields.Integer("Adult Persons" ,)
    child = fields.Integer("Child" ,)
    via = fields.Selection([
        ('direct', 'Direct'),
        ('agent', 'Agent')
        ]) 
    agent_id = fields.Many2one('res.partner',)
    tour_type = fields.Selection([
        ('international', 'International'),
        ('domastic', 'Domastic')],
        string="Tour Type")
    season_id = fields.Many2one('tour.season',"Season" )
    tour_id = fields.Many2one('tour.package','Tour')
    tour_dates_id = fields.Many2one('tour.dates',"Tour Dates" )
    payment_policy_id = fields.Many2one('tour.payment.policy',"Payment Policy" )
    commission_compute = fields.Char("Commission")
    tour_customer_ids = fields.One2many('tour.customer.details','cancel_id',"Tour Customer",  )
    insurance_line_ids = fields.One2many('tour.insurance.line','cancel_id',"Services",  )
    total_insurance_amt = fields.Float('Insuarance Amount', )
    total_amt = fields.Float('Total Amount' )
    tour_cost = fields.Float('Tour Cost')
    tour_sale_order_ids = fields.Many2many('sale.order','tour_book_sale_order_rel','sale_id','book_id', )
    tour_booking_invoice_ids = fields.Many2many('account.move','tour_book_account_invoice_rel','account_id','book_id', )
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)


    def button_request(self):
        for rec in self:
            rec.write({'state':'in_process'})

    def action_done(self):
        for rec in self:
            rec.write({'state':'done'})

    @api.onchange('tour')
    def onchange_tour_id(self):
        for rec in self:
            rec.current_date = rec.tour.current_date
            rec.customer_id = rec.tour.customer_id.id
            rec.email_id = rec.tour.email_id
            rec.mobile1 = rec.tour.mobile1
            rec.adult = rec.tour.adult
            rec.child = rec.tour.child
            rec.via = rec.tour.via
            rec.agent_id = rec.tour.agent_id.id
            rec.tour_type = rec.tour.tour_type
            rec.season_id = rec.tour.season_id.id
            rec.tour_id = rec.tour.tour_id.id
            rec.tour_dates_id = rec.tour.tour_dates_id.id
            rec.payment_policy_id = rec.tour.payment_policy_id.id
            rec.total_amt = rec.tour.subtotal
            rec.total_insurance_amt = rec.tour.total_insurance_amt

    @api.model
    def create(self,vals):
        obj = self.env['tour.booking'].browse(vals.get('tour'))
        vals['name'] = self.env['ir.sequence'].get('tour.cancel') or '/'
        vals['current_date']=obj.current_date
        vals['customer_id']=obj.customer_id.id
        vals['email_id']=obj.email_id
        vals['mobile1']=obj.mobile1
        vals['adult']=obj.adult
        vals['child']=obj.child
        vals['via']=obj.via
        vals['agent_id']=obj.agent_id.id
        vals['tour_type']=obj.tour_type
        vals['season_id']=obj.season_id.id
        vals['tour_id']=obj.tour_id.id
        vals['tour_dates_id']=obj.tour_dates_id.id
        vals['payment_policy_id']=obj.payment_policy_id.id
        vals['total_amt']=obj.total_amt
        vals['total_insurance_amt']=obj.total_insurance_amt
        ids = [a.id for a in obj.tour_customer_ids]
        vals['tour_customer_ids'] = [(6, 0, ids)]
        res = super(tour_cancellation, self).create(vals)
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
