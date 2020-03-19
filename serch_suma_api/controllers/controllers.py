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

        jid = int(jid)
        amount = kw.get('Monto', False) or kw.get('monto', False)
        if not amount:
            return json.dumps({
                _('status'): 404,
                _('message'): _("Amount missing! Please, provide 'monto'.")
            })

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

        ref = kw.get('Referencia', False) or kw.get('referencia', False)
        move_to_find = [
            ('name', '=', kw.get('Folio', False) or kw.get('folio', False)),
            ('invoice_date', '=', invoice_date),
        ]

        moves = Move.search(move_to_find)
        payments = Payment.search(['&', '&', '&', ('invoice_ids.id', 'in', moves.ids), ('state', '=', 'draft'), ('amount', '=', amount), ('payment_date', '=', payment_date)])

        partner_id = None
        for m in moves:
            partner_id = m['partner_id']
        
        if (len(payments.ids) == 0):
            payments = Payment.create({
                'payment_date': payment_date,
                'partner_type': 'customer',
                'payment_type': 'inbound',
                'payment_method_id': 1,
                'journal_id': jid,
                'amount': amount,
                'state': 'draft',
                'invoice_ids': moves.ids,
                'partner_id': partner_id.id,
                'payment_reference': ref,
            })

            payments.default_get(['company_id', 'payment_method_id', 'journal_id'])

            for m in moves:
                for l in m['line_ids']:
                    for p in payments:
                        l['payment_id'] = p
        
        # print('payments: ', payments.ids)
        # print('moves: ', moves.ids)
        result = None
        try: 
            result = payments.post()
        except Exception as err:
            return json.dumps({
                _('status'): 500,
                _('message'): _("Error: {0}".format(err))
            })

        # print(result)
        return json.dumps({
            _('status'): 200,
            _('message'): result,
        })