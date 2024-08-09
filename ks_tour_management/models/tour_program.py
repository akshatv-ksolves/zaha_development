from odoo import models, fields, api, _

class TourProgram(models.Model):
    _inherit = "tour.program"

    hotel_type_id = fields.Many2one('hotel.type')
    room_type_id = fields.Many2one('room.type')