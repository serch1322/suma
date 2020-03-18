# -*- coding: utf-8 -*-
{
    'name': "serch_suma_api",

    'summary': """
        Payment should be created for the invoice matching the number for above mentioned amount and should be reconciled against that invoice by user with matching uid.
    """,

    'description': """
        REQ#1: Script:

            - Just for getting invoice information, they don't need script. they can just export open invoices with required fields and upload in their SUMA.

        REQ#2: Payment:

            To register payment on invoice URL gets generated/called from SUMA:

            URL: https://serch1322-suma.odoo.com/Aplicar_pago?Fecha=30/01/2020&Folio=V8097&Fecha_Real=25/01/2020&Referencia=Comentarioxxx&Monto=15234 

            Field mapping: 

            1. Payment Date[Fecha]: 30/01/2020 

            2. Invoice Number[Folio] :  V8097 

            3. Invoice Date[Fecha_Real]:   25/01/2020 

            4. Payment Reference[Referencia]: Comentarioxxx

            5. Payment Amount[Monto]:  15,234

            6. uid: id of odoo user.(This additional field we need in order to create payment on invoice).

        Payment should be created for the invoice matching the number for above mentioned amount and should be reconciled against that invoice by user with matching uid.
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Payments',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # only loaded in demonstration mode
    'demo': [],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
}
