# -*- coding: utf-8 -*-

import json
import datetime

from odoo.http import request
from odoo import _, http


class SerchSumaApi(http.Controller):
    @http.route('/aplicar_pago', auth='public')
    def index(self, **kw):

        jid = kw.get('jid', False) or kw.get('JID', False)
        if not jid:
            return json.dumps({
                _('status'): 404,
                _('message'): _("Journal id not found! The 'jid' provided was not found.")
            })

        # 1. Payment Date[Fecha]: 30/01/2020 
        # 2. Invoice Number[Folio] :  V8097 
        # 3. Invoice Date[Fecha_Real]:   25/01/2020 
        # 4. Payment Reference[Referencia]: Comentarioxxx
        # 5. Payment Amount[Monto]:  15,234

        # def action_invoice_register_payment(self):
        #     return self.env['account.payment']\
        #         .with_context(active_ids=self.ids, active_model='account.move', active_id=self.id)\
        #         .action_register_payment()


        invoice_date = kw.get('Fecha_Real', False) or kw.get('fecha_real', False)
        payment_date = kw.get('Fecha', False) or kw.get('fecha', False)

        if not invoice_date or not payment_date:
            return json.dumps({
                _('status'): 404,
                _('message'): _("Invoice date or Payment date is missing! Please, provide both.")
            })

        invoice_date = list(map(lambda x: int(x), invoice_date.split('/')))
        invoice_date = datetime.date(invoice_date[2], invoice_date[1], invoice_date[0])

        payment_date = list(map(lambda x: int(x), payment_date.split('/')))
        payment_date = datetime.date(payment_date[2], payment_date[1], payment_date[0])
        
        Move = request.env['account.move'].sudo()
        Payment = request.env['account.payment'].sudo()
        journal_id = request.env['account.journal'].sudo().search([('id', '=', jid)])

        move_to_find = [
            ('name', '=', kw.get('Folio', False) or kw.get('folio', False)),
            ('invoice_payment_ref', '=', kw.get('Referencia', False) or kw.get('referencia', False)),
            ('invoice_date', '=', invoice_date),
        ]

        moves = Move.search(move_to_find)
        payments = Payment.search([('invoice_ids.id', 'in', moves.ids)])

        others = Payment.search([])
        print(others)
        for o in others:
            print(o['name'])
        
        print(moves.ids)
        print(payments)
        for p in payments:
            p['journal_id'] = journal_id
            p['payment_date'] = payment_date
            p['amount'] = kw.get('Monto', False) or kw.get('monto', False)

        result = None
        try: 
            result = payments.post()
        except Exception as err:
            return json.dumps({
                _('status'): 500,
                _('message'): _("Error: {0}".format(err))
            })

        print(result)
        return json.dumps({
            _('status'): 200,
            _('message'): result,
        })