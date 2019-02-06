# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import models, api






class pos_pdf_report(models.AbstractModel):
    _name = 'report.bi_inventory_pos_report.pos_fast_moving_pdf_template'
    
    @api.multi
    def _get_report_values(self, docids, data=None):
        data = data if data is not None else {}
        docs = self.env['pos.fast.moving.wizard'].browse(docids)
        data  = { 'start_date': docs.start_date, 'end_date': docs.end_date,
                'warehouse_id':docs.warehouse_id
                }
        
        return {
                   'doc_model': 'pos.fast.moving.wizard',
                   'data' : data,

                   
                   'get_lines':self._get_lines(data),
                   
                   
                   }



   


    def _get_lines(self,data):

      vals = []
      domain = [('order_id.state','in',['done','paid'])]
      if data['start_date'] :
        domain.append(('order_id.date_order','>=',data['start_date']))
      if data['end_date'] :

        domain.append(('order_id.date_order','<=',data['end_date']))

      # if data['branch_id'] :
      #   domain.append(('order_id.branch_id','=',data['branch_id'].id))
      pos_line_rec = self.env['pos.order.line'].search(domain)

      
      for line in pos_line_rec :
        warehouse = self.env['stock.warehouse'].search([('branch_id','=',line.order_id.branch_id.id)])
        if warehouse.id == data['warehouse_id'].id:
          vals.append({'name' : line.product_id.name,
                      'code' : line.product_id.default_code,
                      'sale_qty' : line.qty,
                      'gross_price': line.price_unit * line.qty,
                      'discount' : line.discount,
                      'net_sales' : line.price_subtotal,
                      'vat' : line.tax_ids_after_fiscal_position.amount,
                      'total' : line.price_subtotal_incl
                      })


     
      return vals


