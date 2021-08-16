# -*- coding: utf-8 -*-
# from odoo import http


# class EpidemicRecord(http.Controller):
#     @http.route('/epidemic_record/epidemic_record/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/epidemic_record/epidemic_record/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('epidemic_record.listing', {
#             'root': '/epidemic_record/epidemic_record',
#             'objects': http.request.env['epidemic_record.epidemic_record'].search([]),
#         })

#     @http.route('/epidemic_record/epidemic_record/objects/<model("epidemic_record.epidemic_record"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('epidemic_record.object', {
#             'object': obj
#         })
