
class CreateSCASales(http.Controller):
    @http.route('/data/SCA/CreateSCASales', type='json', csrf=False, auth='public')
    def CreateSCASales(self, **rec):
        so_numbers = []
        credit_note_no = []
        for row in rec["data"]:
            order_type = row["master"]["order_type"]
            invoice_ref = row["master"]["orderID"]
            #             invoice_ref_true = request.env['sale.order'].sudo().search(
            #                             [('client_order_ref', '=', invoice_ref)], limit=1)
            #             if invoice_ref_true:
            #                 so_numbers.append({
            #                                     'orderID': invoice_ref_true.client_order_ref,
            #                                     'soNumber': invoice_ref_true.name
            #                                 })
            #             else:
            if order_type == "NORMAL":
                invoice_ref_true = request.env['sale.order'].sudo().search([('client_order_ref', '=', invoice_ref)], limit=1)
                if invoice_ref_true:
                    so_numbers.append({
                        'orderID': invoice_ref_true.client_order_ref,
                        'soNumber': invoice_ref_true.name
                    })
                else:
                    tax_type = row["master"]["partner_id"]["tax_type"]

                    customer_name = "Route Collection"
                    customer_type = row["master"]["customer_type"]

                    invoice_date = row["master"]["date"]
                    date = datetime.strptime(invoice_date, '%d/%m/%Y')

                    # customer_ref = row["master"]["partner_id"]["ref"]
                    from_company_detail = request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                    if customer_name:
                        customer = customer_name and request.env['res.partner'].sudo().search(
                            [('name', '=', customer_name)], limit=1) or False
                        if not customer:
                            raise ValidationError(_("Customer not found"))
                    order_line = []
                    for product_line in row["child"]:
                        product_item = product_line["name"]
                        gst = product_line["cgst"] + product_line["sgst"]
                        igst = product_line["igst"]
                        tax = False
                        tax_variant = False
                        if gst:
                            tax_variant = request.env['account.tax'].sudo().search(
                                [('company_id', '=', from_company_detail.id), ('amount', '=', str(gst)),
                                 ('type_tax_use', '=', "sale"),
                                 ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                        if igst:
                            tax_variant = request.env['account.tax'].sudo().search(
                                [('company_id', '=', from_company_detail.id), ('amount', '=', str(igst)),
                                 ('type_tax_use', '=', "sale"),
                                 ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                        tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                        if product_item:
                            product = product_item and request.env['product.product'].sudo().search(
                                [('name', '=', product_item)], limit=1) or False
                            uom_ids = request.env['uom.uom'].sudo().search([])
                            unit_id = request.env.ref('uom.product_uom_unit') and request.env.ref(
                                'uom.product_uom_unit').id or False
                            for record in uom_ids:
                                if record.name == "kg":
                                    unit_id = record.id
                            if not product:
                                so_numbers.append({
                                    'status': "Product Not Found",
                                    'Product Name': product_item,
                                    'orderID': row["master"]["orderID"]
                                })

                        if product:
                            order_line.append((0, 0, {
                                'display_type': False,
                                # 'sequence': 10,
                                'product_id': product.id,
                                'name': product.name or '',
                                # 'date_planned': row.TRANSACTION_DATE or False,
                                # 'account_analytic_id': False,
                                'product_uom_qty': product_line["product_qty"] or 0,
                                # 'qty_received_manual': 0,
                                #                             'discount': False,
                                #                             'discount': ((product_line["discount"] * 100)) / (
                                #                             (product_line["product_qty"] * product_line["rate"])) or 0,
                                'discount_method': 'fix',
                                'discount_amount': product_line["discount"],
                                'product_uom': product.uom_id.id or request.env.ref(
                                    'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                                'price_unit': product_line["rate"] or 0,
                                'tax_id': tax,
                            }))
                    if customer:
                        if tax_type == "INTRA":
                            jounalname = "Route Sales - Intra State"
                            coaname = "Sales GST - Intra State (Route Sales)"
                        elif tax_type == "INTER":
                            jounalname = "Route Sales - Inter State"
                            coaname = "Sales GST - Inter State (Route Sales)"
                        else:
                            raise ValidationError(_("Journal not found"))

                        jounal_id = jounalname and request.env['account.journal'].sudo().search(
                            [('name', '=', jounalname), ('company_id', '=', from_company_detail.id)], limit=1) or False
                        coa = coaname and request.env['account.account'].sudo().search(
                            [('name', '=', coaname), ('company_id', '=', from_company_detail.id)], limit=1) or False
                        code = row["master"]["partner_id"]["ref"]
                        if code:
                            route = row["master"]["partner_id"]["name"]
                            route_code = row["master"]["partner_id"]["ref"]

                            analytical_id = request.env['account.analytic.account'].sudo().search(
                                [('code', 'like', code), ('company_id', '=', from_company_detail.id)], limit=1) or False
                            if not analytical_id:
                                analytical_details = {
                                    'name': row["master"]["partner_id"]["ref"],
                                    'code': row["master"]["partner_id"]["name"] + " - " + row["master"]["partner_id"][
                                        "ref"],
                                    'company_id': from_company_detail.id,
                                }
                                analytical_id = request.env['account.analytic.account'].sudo().create \
                                    (analytical_details)
                                request.env.cr.commit()
                            analytical_id = request.env['account.analytic.account'].sudo().search(
                                [('code', 'like', code), ('company_id', '=', from_company_detail.id)], limit=1) or False
                        sale_order_1 = request.env['sale.order'].sudo().create({
                            'partner_id': customer.id,
                            'client_order_ref': row["master"]["orderID"] or '',
                            # 'origin': row.INVOICE_NUM or '',
                            'date_order': date,
                            # 'date_planned':date,
                            'analytic_account_id': analytical_id.id,
                            'l10n_in_journal_id': jounal_id.id,
                            'l10n_in_gst_treatment': customer_type,
                            # 'partner_id': self.env.ref('base.main_partner').id,
                            # 'name': row.INVOICE_NUM or '',
                            'discount_type': 'line',
                            'order_line': order_line,
                            'company_id': from_company_detail.id
                        })
                        request.env.cr.commit()

                        try:
                            if sale_order_1:
                                sale_order_1.l10n_in_gst_treatment = customer_type
                                sale_order_1.action_confirm()
                                sale_order_1.date_order = date
                                sale_order_1.l10n_in_journal_id = jounal_id.id

                                pick_name = "Route Sale Delivery Orders"

                                picking_type = request.env['stock.picking.type'].sudo().search([('name', '=', pick_name),
                                    ('company_id', '=', from_company_detail.id)],
                                                    limit=1)

                                source_location = request.env['stock.location'].sudo().search(
                                    [('loc_code', '=', route_code), ('company_id', '=', from_company_detail.id)], limit=1)
                                if sale_order_1.picking_ids:
                                    sale_order_1.picking_ids.action_toggle_is_locked()
                                    for picking in sale_order_1.picking_ids:
                                        picking.scheduled_date = date
                                        picking.location_id = source_location.id

                                        picking.picking_type_id = picking_type.id

                                        picking.do_unreserve()
                                        request.env.cr.commit()
                                        picking.action_assign()
                                        for line_ids in picking.move_line_ids:
                                            line_ids.location_id = source_location.id
                                            line_ids.qty_done = line_ids.product_uom_qty
                                        request.env.cr.commit()
                                        picking.button_validate()

                                    for so in sale_order_1.picking_ids:
                                        so.date = date
                                        if (so.date_done):
                                            if (so.state != "done"):
                                                so.scheduled_date = date
                                            if (so.state == "done"):
                                                so.date_done = date
                                        for line_ids in so.move_line_ids:
                                            line_ids.date = date
                                            line_ids.move_id.date = date

                                        request.env.cr.commit()
                                    invoice = sale_order_1._create_invoices(final=True)
                                    #                                     if sale_order_1._create_invoices(final=True):
                                    invoice.l10n_in_gst_treatment = customer_type
                                    invoice.invoice_date = date
                                    invoice.date = date
                                    invoice.invoice_date_due = date
                                    for inv_lines in invoice.invoice_line_ids:
                                        inv_lines.analytic_account_id = analytical_id.id
                                        inv_lines.account_id = coa.id
                                    for inv_journal_lines in invoice.line_ids:
                                        #                                     if inv_journal_lines.name == "Discount":
                                        inv_journal_lines.analytic_account_id = analytical_id.id
                                    invoice.action_post()
                                    so_numbers.append({
                                        'orderID': row["master"]["orderID"],
                                        'soNumber': sale_order_1.name,
                                        'status': "Success"
                                    })
                        #                                     else:
                        #                                         so_numbers.append({
                        #                                             'orderID': row["master"]["orderID"],
                        #                                             'soNumber': sale_order_1.name,
                        #                                             'status': "Error"
                        #                                         })
                        except Exception:
                            error_msg = _("Error")
                            #                                 raise self.env['res.config.settings'].get_config_warning(error_msg)

                            so_numbers.append({
                                'orderID': row["master"]["orderID"],
                                'soNumber': sale_order_1.name,
                                'status': error_msg
                            })
            #                                 so_numbers.append({
            #                                     'orderID': row["master"]["orderID"],
            #                                     'soNumber': sale_order_1.name
            #                                 })
            #                     if sale_order_1:
            #                         sale_order_1.date_order = date
            #                         sale_order_1.l10n_in_gst_treatment = customer_type
            #                         sale_order_1.action_confirm()
            #                         sale_order_1.date_order = date
            #                         sale_order_1.l10n_in_journal_id = jounal_id.id
            #                         source_location = request.env['stock.location'].sudo().search(
            #                             [('name', 'like', route), ('company_id', '=', from_company_detail.id)], limit=1)
            #                         if sale_order_1.picking_ids:
            #                             sale_order_1.picking_ids.action_toggle_is_locked()
            #                             for picking in sale_order_1.picking_ids:
            #                                 picking.location_id = source_location.id
            #                                 picking.do_unreserve()
            #                                 request.env.cr.commit()
            #                                 picking.action_assign()
            #                                 for line_ids in picking.move_line_ids:
            #                                     line_ids.location_id = source_location.id
            #                                     line_ids.qty_done = line_ids.product_uom_qty
            #                                 request.env.cr.commit()
            #                                 picking.button_validate()
            #                                 request.env.cr.commit()
            #                             invoice = sale_order_1._create_invoices(final=True)
            #                             invoice.l10n_in_gst_treatment = customer_type
            #                             invoice.invoice_date = date
            #                             invoice.invoice_date_due = date
            #                             for inv_lines in invoice.invoice_line_ids:
            #                                 inv_lines.analytic_account_id = analytical_id.id
            #                                 inv_lines.account_id = coa.id
            #                             for inv_journal_lines in invoice.line_ids:
            #                                 if inv_journal_lines.name == "Discount":
            #                                     inv_journal_lines.analytic_account_id = analytical_id.id

            #                         so_numbers.append({
            #                             'orderID': row["master"]["orderID"],
            #                             'soNumber': sale_order_1.name
            #                         })

            elif order_type == "RETURN":
                inv_ref = row["master"]["orderID"]
                invoice_ref = "RB2RS "+ str(inv_ref)
                invoice_ref_true = request.env['account.move'].sudo().search(
                    [('ref', '=', invoice_ref)], limit=1)
                if invoice_ref_true:
                    credit_note_no.append({
                        'orderID': row["master"]["orderID"],
                        'creditNoteNumber': invoice_ref_true.name
                    })
                else:
                    tax_type = row["master"]["partner_id"]["tax_type"]

                    customer_name = "Route Collection"
                    invoice_date = row["master"]["date"]
                    date = datetime.strptime(invoice_date, '%d/%m/%Y')
                    customer_type = row["master"]["customer_type"]

                    to_company_detail2 = request.env['res.company'].sudo().search(
                        [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

                    if tax_type == "INTRA":
                        jounalname = "Route Sales - Intra State"
                        coaname = "Sales GST - Intra State (Route Sales)"
                    elif tax_type == "INTER":
                        jounalname = "Route Sales - Inter State"
                        coaname = "Sales GST - Inter State (Route Sales)"
                    else:
                        raise ValidationError(_("Journal not found"))

                    jounal_id = jounalname and request.env['account.journal'].sudo().search(
                        [('name', '=', jounalname), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                    coa = coaname and request.env['account.account'].sudo().search(
                        [('name', '=', coaname), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                    if customer_name:
                        customer = customer_name and request.env['res.partner'].sudo().search(
                            [('name', '=', customer_name)], limit=1) or False

                        if not customer:
                            raise ValidationError(_("Route not found"))
                        invoice_line_ids = []
                        total_discount_amt = 0
                        for line in row["child"]:
                            product = line["name"]
                            quantity = line["product_qty"]
                            discount = line["discount"]
                            total_discount_amt = total_discount_amt + discount
                            price = line["rate"]
                            gst = line["cgst"] + line["sgst"]
                            igst = line["igst"]
                            tax_variant = False
                            if gst:
                                tax_variant = request.env['account.tax'].sudo().search(
                                    [('company_id', '=', to_company_detail2.id), ('amount', '=', str(gst)),
                                     ('type_tax_use', '=', "purchase"),
                                     ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                            if igst:
                                tax_variant = request.env['account.tax'].sudo().search(
                                    [('company_id', '=', to_company_detail2.id), ('amount', '=', str(igst)),
                                     ('type_tax_use', '=', "purchase"),
                                     ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                            if tax_variant:
                                tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                            else:
                                tax = False
                            product_id = product and request.env['product.product'].sudo().search(
                                [('name', '=', product)], limit=1) or False
                            code = row["master"]["partner_id"]["ref"]
                            if code:
                                analytical_id = request.env['account.analytic.account'].sudo().search(
                                    [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                                if not analytical_id:
                                    analytical_details = {
                                        'name': row["master"]["partner_id"]["name"],
                                        'code': row["master"]["partner_id"]["ref"],
                                        'company_id': to_company_detail2.id,
                                    }
                                    analytical_id = request.env['account.analytic.account'].sudo().create(
                                        analytical_details)
                                analytical_id = request.env['account.analytic.account'].sudo().search(
                                    [('code', 'like', code), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                            invoice_line_ids.append((0, 0, {
                                'display_type': False,
                                'quantity': quantity,
                                'product_id': product_id,
                                'product_uom_id': product_id.uom_id.id,
                                'price_unit': price,
                                'discount_method': 'fix',
                                'discount_amount': discount,
                                'tax_ids': tax_variant,
                                'analytic_account_id': analytical_id,
                                'account_id' : coa.id
                            }))
                    if customer:
                        credit_note_1 = request.env['account.move'].sudo().create({
                            'move_type': "out_refund",
                            'partner_id': customer.id,
                            'company_id': to_company_detail2.id,
                            'journal_id': jounal_id.id,
                            'invoice_date': date,
                            'discount_type': 'line',
                            'discount_amt_line': total_discount_amt,
                            'date': date,
                            'invoice_line_ids': invoice_line_ids,
                            'ref': invoice_ref
                        })
                        request.env.cr.commit()

                        if credit_note_1:
                            credit_note_1.l10n_in_gst_treatment = customer_type
                            for inv_journal_lines in credit_note_1.line_ids:
                                #                                 if inv_journal_lines.name == "Discount":
                                inv_journal_lines.analytic_account_id = analytical_id.id
                            credit_note_1.action_post()
                            credit_note_no.append({
                                'orderID': row["master"]["orderID"],
                                'creditNoteNumber': credit_note_1.name
                            })

                            destination_code = row["master"]["partner_id"]["ref"]
                            source = credit_note_1.name
                            picking_name = "Van Returns"

                            company_id = request.env['res.company'].sudo().search \
                                ([('name', '=', "Eastea Chai Private Limited (KL)")], limit=1) or False
                            picking_type = request.env['stock.picking.type'].sudo().search \
                                ([('name', '=', picking_name), ('company_id', '=', company_id.id)], limit=1) or False
                            location_dest_id = request.env['stock.location'].sudo().search \
                                ([('loc_code', '=', destination_code), ('company_id', '=', company_id.id)], limit=1) or False
                            location_id = request.env['stock.location'].sudo().search \
                                ([('loc_code', 'like', "CustomerLocation")], limit=1) or False

                            picking = request.env['stock.picking'].sudo().create({
                                'location_id': location_id.id,
                                'location_dest_id': location_dest_id.id,
                                # 'partner_id': self.test_partner.id,
                                'picking_type_id': picking_type.id,
                                'immediate_transfer': False,
                                'ref': "SCA - " + str(source) + "-" + str(destination_code),
                                'company_id': company_id.id,
                                'origin': source
                            })
                            move_receipt_1 = []
                            for line in row["child"]:
                                product_item = line["name"]
                                if product_item:
                                    product = product_item and request.env['product.product'].sudo().search(
                                        [('name', '=', product_item)], limit=1) or False
                                    product_lot_number = "RET-" + str(source) + "-" + str(destination_code) + str \
                                        (product.id)
                                    lot_no = request.env['stock.production.lot'].sudo().search \
                                        ([('company_id', '=', company_id.id), ('name', '=', product_lot_number)])
                                    if not lot_no:
                                        lot_number = {
                                            'name': product_lot_number,
                                            'product_id': product.id,
                                            'company_id': company_id.id
                                        }
                                        create_lot_number = request.env['stock.production.lot'].sudo().create \
                                            (lot_number)
                                    lot_no = request.env['stock.production.lot'].sudo().search(
                                        [('company_id', '=', company_id.id), ('name', '=', product_lot_number)])
                                    if product:
                                        move_receipt_1 = request.env['stock.move'].sudo().create({
                                            'name': product.name,
                                            'product_id': product.id,
                                            'product_uom_qty': line["product_qty"],
                                            'quantity_done': line["product_qty"],
                                            'product_uom': product.uom_id.id,
                                            'picking_id': picking.id,
                                            'picking_type_id': picking_type.id,
                                            'location_id': location_id.id,
                                            'location_dest_id': location_dest_id.id,
                                            'company_id': company_id.id
                                        })
                                        request.env.cr.commit()
                                        move_receipt_line = request.env['stock.move.line'].sudo().search(
                                            [('move_id', '=', move_receipt_1.id)], limit=1)

                                        move_receipt_line.lot_id = lot_no.id
                                        move_receipt_line.lot_name = lot_no.name

                            picking.action_confirm()
                            picking.button_validate()

        return credit_note_no, so_numbers

    class CreateSCASalesTest(http.Controller):
        @http.route('/data/SCA/CreateSCASales/test', type='json', csrf=False, auth='public')
        def CreateSCASales(self, **rec):
            so_numbers = []
            credit_note_no = []
            for row in rec["data"]:
                order_type = row["master"]["order_type"]
                invoice_ref = row["master"]["orderID"]
                #             invoice_ref_true = request.env['sale.order'].sudo().search(
                #                             [('client_order_ref', '=', invoice_ref)], limit=1)
                #             if invoice_ref_true:
                #                 so_numbers.append({
                #                                     'orderID': invoice_ref_true.client_order_ref,
                #                                     'soNumber': invoice_ref_true.name
                #                                 })
                #             else:
                if order_type == "NORMAL":
                    invoice_ref_true = request.env['sale.order'].sudo().search([('client_order_ref', '=', invoice_ref)],
                                                                               limit=1)
                    if invoice_ref_true:
                        so_numbers.append({
                            'orderID': invoice_ref_true.client_order_ref,
                            'soNumber': invoice_ref_true.name
                        })
                    else:
                        tax_type = row["master"]["partner_id"]["tax_type"]

                        customer_name = "Route Collection"
                        customer_type = row["master"]["customer_type"]

                        invoice_date = row["master"]["date"]
                        date = datetime.strptime(invoice_date, '%d/%m/%Y')

                        # customer_ref = row["master"]["partner_id"]["ref"]
                        from_company_detail = request.env['res.company'].sudo().search(
                            [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False
                        if customer_name:
                            customer = customer_name and request.env['res.partner'].sudo().search(
                                [('name', '=', customer_name)], limit=1) or False
                            if not customer:
                                raise ValidationError(_("Customer not found"))
                        order_line = []
                        for product_line in row["child"]:
                            product_item = product_line["name"]
                            gst = product_line["cgst"] + product_line["sgst"]
                            igst = product_line["igst"]
                            tax = False
                            tax_variant = False
                            if gst:
                                tax_variant = request.env['account.tax'].sudo().search(
                                    [('company_id', '=', from_company_detail.id), ('amount', '=', str(gst)),
                                     ('type_tax_use', '=', "sale"),
                                     ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                            if igst:
                                tax_variant = request.env['account.tax'].sudo().search(
                                    [('company_id', '=', from_company_detail.id), ('amount', '=', str(igst)),
                                     ('type_tax_use', '=', "sale"),
                                     ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                            tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                            if product_item:
                                product = product_item and request.env['product.product'].sudo().search(
                                    [('name', '=', product_item)], limit=1) or False
                                uom_ids = request.env['uom.uom'].sudo().search([])
                                unit_id = request.env.ref('uom.product_uom_unit') and request.env.ref(
                                    'uom.product_uom_unit').id or False
                                for record in uom_ids:
                                    if record.name == "kg":
                                        unit_id = record.id
                                if not product:
                                    so_numbers.append({
                                        'status': "Product Not Found",
                                        'Product Name': product_item,
                                        'orderID': row["master"]["orderID"]
                                    })

                            if product:
                                order_line.append((0, 0, {
                                    'display_type': False,
                                    # 'sequence': 10,
                                    'product_id': product.id,
                                    'name': product.name or '',
                                    # 'date_planned': row.TRANSACTION_DATE or False,
                                    # 'account_analytic_id': False,
                                    'product_uom_qty': product_line["product_qty"] or 0,
                                    # 'qty_received_manual': 0,
                                    #                             'discount': False,
                                    #                             'discount': ((product_line["discount"] * 100)) / (
                                    #                             (product_line["product_qty"] * product_line["rate"])) or 0,
                                    'discount_method': 'fix',
                                    'discount_amount': product_line["discount"],
                                    'product_uom': product.uom_id.id or request.env.ref(
                                        'uom.product_uom_unit') and request.env.ref('uom.product_uom_unit').id or False,
                                    'price_unit': product_line["rate"] or 0,
                                    'tax_id': tax,
                                }))
                        if customer:
                            if tax_type == "INTRA":
                                jounalname = "Route Sales - Intra State"
                                coaname = "Sales GST - Intra State (Route Sales)"
                            elif tax_type == "INTER":
                                jounalname = "Route Sales - Inter State"
                                coaname = "Sales GST - Inter State (Route Sales)"
                            else:
                                raise ValidationError(_("Journal not found"))

                            jounal_id = jounalname and request.env['account.journal'].sudo().search(
                                [('name', '=', jounalname), ('company_id', '=', from_company_detail.id)],
                                limit=1) or False
                            coa = coaname and request.env['account.account'].sudo().search(
                                [('name', '=', coaname), ('company_id', '=', from_company_detail.id)], limit=1) or False
                            code = row["master"]["partner_id"]["ref"]
                            if code:
                                route = row["master"]["partner_id"]["name"]
                                route_code = row["master"]["partner_id"]["ref"]

                                analytical_id = request.env['account.analytic.account'].sudo().search(
                                    [('code', 'like', code), ('company_id', '=', from_company_detail.id)],
                                    limit=1) or False
                                if not analytical_id:
                                    analytical_details = {
                                        'name': row["master"]["partner_id"]["ref"],
                                        'code': row["master"]["partner_id"]["name"] + " - " +
                                                row["master"]["partner_id"][
                                                    "ref"],
                                        'company_id': from_company_detail.id,
                                    }
                                    analytical_id = request.env['account.analytic.account'].sudo().create(
                                        analytical_details)
                                    request.env.cr.commit()
                                analytical_id = request.env['account.analytic.account'].sudo().search(
                                    [('code', 'like', code), ('company_id', '=', from_company_detail.id)],
                                    limit=1) or False
                            sale_order_1 = request.env['sale.order'].sudo().create({
                                'partner_id': customer.id,
                                'client_order_ref': row["master"]["orderID"] or '',
                                # 'origin': row.INVOICE_NUM or '',
                                'date_order': date,
                                # 'date_planned':date,
                                'analytic_account_id': analytical_id.id,
                                'l10n_in_journal_id': jounal_id.id,
                                'l10n_in_gst_treatment': customer_type,
                                # 'partner_id': self.env.ref('base.main_partner').id,
                                # 'name': row.INVOICE_NUM or '',
                                'discount_type': 'line',
                                'order_line': order_line,
                                'company_id': from_company_detail.id
                            })
                            request.env.cr.commit()

                            try:
                                if sale_order_1:
                                    sale_order_1.l10n_in_gst_treatment = customer_type
                                    sale_order_1.action_confirm()
                                    sale_order_1.date_order = date
                                    sale_order_1.l10n_in_journal_id = jounal_id.id
                                    source_location = request.env['stock.location'].sudo().search(
                                        [('loc_code', '=', route_code), ('company_id', '=', from_company_detail.id)],
                                        limit=1)
                                    if sale_order_1.picking_ids:
                                        sale_order_1.picking_ids.action_toggle_is_locked()
                                        for picking in sale_order_1.picking_ids:

                                            picking_name = "Route Sale Delivery Orders"
                                            company_id = request.env['res.company'].sudo().search(
                                                [('name', '=', "Eastea Chai Private Limited (KL)")], limit=1) or False
                                            picking_type = request.env['stock.picking.type'].sudo().search(
                                                [('name', '=', picking_name), ('company_id', '=', company_id.id)],
                                                limit=1) or False
                                            picking.picking_type_id = picking_type.id
                                            picking.scheduled_date = date
                                            picking.location_id = source_location.id
                                            picking.do_unreserve()
                                            request.env.cr.commit()
                                            picking.action_assign()
                                            for line_ids in picking.move_line_ids:
                                                line_ids.location_id = source_location.id
                                                line_ids.qty_done = line_ids.product_uom_qty
                                            request.env.cr.commit()
                                            picking.button_validate()

                                        for so in sale_order_1.picking_ids:
                                            so.date = date
                                            if (so.date_done):
                                                if (so.state != "done"):
                                                    so.scheduled_date = date
                                                if (so.state == "done"):
                                                    so.date_done = date
                                            for line_ids in so.move_line_ids:
                                                line_ids.date = date
                                                line_ids.move_id.date = date

                                            request.env.cr.commit()
                                        invoice = sale_order_1._create_invoices(final=True)
                                        #                                     if sale_order_1._create_invoices(final=True):
                                        invoice.l10n_in_gst_treatment = customer_type
                                        invoice.invoice_date = date
                                        invoice.date = date
                                        invoice.invoice_date_due = date
                                        for inv_lines in invoice.invoice_line_ids:
                                            inv_lines.analytic_account_id = analytical_id.id
                                            inv_lines.account_id = coa.id
                                        for inv_journal_lines in invoice.line_ids:
                                            #                                     if inv_journal_lines.name == "Discount":
                                            inv_journal_lines.analytic_account_id = analytical_id.id
                                        invoice.action_post()
                                        so_numbers.append({
                                            'orderID': row["master"]["orderID"],
                                            'soNumber': sale_order_1.name,
                                            'status': "Success"
                                        })
                            #                                     else:
                            #                                         so_numbers.append({
                            #                                             'orderID': row["master"]["orderID"],
                            #                                             'soNumber': sale_order_1.name,
                            #                                             'status': "Error"
                            #                                         })
                            except Exception:
                                error_msg = _("Error")
                                #                                 raise self.env['res.config.settings'].get_config_warning(error_msg)

                                so_numbers.append({
                                    'orderID': row["master"]["orderID"],
                                    'soNumber': sale_order_1.name,
                                    'status': error_msg
                                })
                #                                 so_numbers.append({
                #                                     'orderID': row["master"]["orderID"],
                #                                     'soNumber': sale_order_1.name
                #                                 })
                #                     if sale_order_1:
                #                         sale_order_1.date_order = date
                #                         sale_order_1.l10n_in_gst_treatment = customer_type
                #                         sale_order_1.action_confirm()
                #                         sale_order_1.date_order = date
                #                         sale_order_1.l10n_in_journal_id = jounal_id.id
                #                         source_location = request.env['stock.location'].sudo().search(
                #                             [('name', 'like', route), ('company_id', '=', from_company_detail.id)], limit=1)
                #                         if sale_order_1.picking_ids:
                #                             sale_order_1.picking_ids.action_toggle_is_locked()
                #                             for picking in sale_order_1.picking_ids:
                #                                 picking.location_id = source_location.id
                #                                 picking.do_unreserve()
                #                                 request.env.cr.commit()
                #                                 picking.action_assign()
                #                                 for line_ids in picking.move_line_ids:
                #                                     line_ids.location_id = source_location.id
                #                                     line_ids.qty_done = line_ids.product_uom_qty
                #                                 request.env.cr.commit()
                #                                 picking.button_validate()
                #                                 request.env.cr.commit()
                #                             invoice = sale_order_1._create_invoices(final=True)
                #                             invoice.l10n_in_gst_treatment = customer_type
                #                             invoice.invoice_date = date
                #                             invoice.invoice_date_due = date
                #                             for inv_lines in invoice.invoice_line_ids:
                #                                 inv_lines.analytic_account_id = analytical_id.id
                #                                 inv_lines.account_id = coa.id
                #                             for inv_journal_lines in invoice.line_ids:
                #                                 if inv_journal_lines.name == "Discount":
                #                                     inv_journal_lines.analytic_account_id = analytical_id.id

                #                         so_numbers.append({
                #                             'orderID': row["master"]["orderID"],
                #                             'soNumber': sale_order_1.name
                #                         })

                elif order_type == "RETURN":
                    inv_ref = row["master"]["orderID"]
                    invoice_ref = "RB2RS" + str(inv_ref)
                    invoice_ref_true = request.env['account.move'].sudo().search(
                        [('ref', '=', invoice_ref)], limit=1)
                    if invoice_ref_true:
                        credit_note_no.append({
                            'orderID': row["master"]["orderID"],
                            'creditNoteNumber': invoice_ref_true.name
                        })
                    else:
                        tax_type = row["master"]["partner_id"]["tax_type"]

                        customer_name = "Route Collection"
                        invoice_date = row["master"]["date"]
                        date = datetime.strptime(invoice_date, '%d/%m/%Y')
                        customer_type = row["master"]["customer_type"]

                        to_company_detail2 = request.env['res.company'].sudo().search(
                            [('name', '=', 'Eastea Chai Private Limited (KL)')], limit=1) or False

                        if tax_type == "INTRA":
                            jounalname = "Route Sales - Intra State"
                            coaname = "Sales GST - Intra State (Route Sales)"
                        elif tax_type == "INTER":
                            jounalname = "Route Sales - Inter State"
                            coaname = "Sales GST - Inter State (Route Sales)"
                        else:
                            raise ValidationError(_("Journal not found"))

                        jounal_id = jounalname and request.env['account.journal'].sudo().search(
                            [('name', '=', jounalname), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        coa = coaname and request.env['account.account'].sudo().search(
                            [('name', '=', coaname), ('company_id', '=', to_company_detail2.id)], limit=1) or False
                        if customer_name:
                            customer = customer_name and request.env['res.partner'].sudo().search(
                                [('name', '=', customer_name)], limit=1) or False

                            if not customer:
                                raise ValidationError(_("Route not found"))
                            invoice_line_ids = []
                            total_discount_amt = 0
                            for line in row["child"]:
                                product = line["name"]
                                quantity = line["product_qty"]
                                discount = line["discount"]
                                total_discount_amt = total_discount_amt + discount
                                price = line["rate"]
                                gst = line["cgst"] + line["sgst"]
                                igst = line["igst"]
                                tax_variant = False
                                if gst:
                                    tax_variant = request.env['account.tax'].sudo().search(
                                        [('company_id', '=', to_company_detail2.id), ('amount', '=', str(gst)),
                                         ('type_tax_use', '=', "purchase"),
                                         ('name', '=', "GST " + str(int(float(gst))) + "%")], limit=1)
                                if igst:
                                    tax_variant = request.env['account.tax'].sudo().search(
                                        [('company_id', '=', to_company_detail2.id), ('amount', '=', str(igst)),
                                         ('type_tax_use', '=', "purchase"),
                                         ('name', '=', "IGST " + str(int(float(igst))) + "%")], limit=1)
                                if tax_variant:
                                    tax = tax_variant and [(6, 0, [tax_variant.id])] or [] or False
                                else:
                                    tax = False
                                product_id = product and request.env['product.product'].sudo().search(
                                    [('name', '=', product)], limit=1) or False
                                code = row["master"]["partner_id"]["ref"]
                                if code:
                                    analytical_id = request.env['account.analytic.account'].sudo().search(
                                        [('code', 'like', code), ('company_id', '=', to_company_detail2.id)],
                                        limit=1) or False
                                    if not analytical_id:
                                        analytical_details = {
                                            'name': row["master"]["partner_id"]["name"],
                                            'code': row["master"]["partner_id"]["ref"],
                                            'company_id': to_company_detail2.id,
                                        }
                                        analytical_id = request.env['account.analytic.account'].sudo().create(
                                            analytical_details)
                                    analytical_id = request.env['account.analytic.account'].sudo().search(
                                        [('code', 'like', code), ('company_id', '=', to_company_detail2.id)],
                                        limit=1) or False
                                invoice_line_ids.append((0, 0, {
                                    'display_type': False,
                                    'quantity': quantity,
                                    'product_id': product_id,
                                    'product_uom_id': product_id.uom_id.id,
                                    'price_unit': price,
                                    'discount_method': 'fix',
                                    'discount_amount': discount,
                                    'tax_ids': tax_variant,
                                    'analytic_account_id': analytical_id,
                                    'account_id': coa.id
                                }))
                        if customer:
                            credit_note_1 = request.env['account.move'].sudo().create({
                                'move_type': "out_refund",
                                'partner_id': customer.id,
                                'company_id': to_company_detail2.id,
                                'journal_id': jounal_id.id,
                                'invoice_date': date,
                                'discount_type': 'line',
                                'discount_amt_line': total_discount_amt,
                                'date': date,
                                'invoice_line_ids': invoice_line_ids,
                                'ref': invoice_ref
                            })
                            request.env.cr.commit()

                            if credit_note_1:
                                credit_note_1.l10n_in_gst_treatment = customer_type
                                for inv_journal_lines in credit_note_1.line_ids:
                                    #                                 if inv_journal_lines.name == "Discount":
                                    inv_journal_lines.analytic_account_id = analytical_id.id
                                credit_note_1.action_post()
                                credit_note_no.append({
                                    'orderID': row["master"]["orderID"],
                                    'creditNoteNumber': credit_note_1.name
                                })

                                destination_code = row["master"]["partner_id"]["ref"]
                                source = credit_note_1.name
                                picking_name = "Van Returns"

                                company_id = request.env['res.company'].sudo().search(
                                    [('name', '=', "Eastea Chai Private Limited (KL)")], limit=1) or False
                                picking_type = request.env['stock.picking.type'].sudo().search(
                                    [('name', '=', picking_name), ('company_id', '=', company_id.id)], limit=1) or False
                                location_dest_id = request.env['stock.location'].sudo().search(
                                    [('loc_code', '=', destination_code), ('company_id', '=', company_id.id)],
                                    limit=1) or False
                                location_id = request.env['stock.location'].sudo().search(
                                    [('loc_code', 'like', "CustomerLocation")], limit=1) or False

                                picking = request.env['stock.picking'].sudo().create({
                                    'location_id': location_id.id,
                                    'location_dest_id': location_dest_id.id,
                                    # 'partner_id': self.test_partner.id,
                                    'picking_type_id': picking_type.id,
                                    'immediate_transfer': False,
                                    'ref': "SCA - " + str(source) + "-" + str(destination_code),
                                    'company_id': company_id.id,
                                    'origin': source
                                })
                                move_receipt_1 = []
                                for line in row["child"]:
                                    product_item = line["name"]
                                    if product_item:
                                        product = product_item and request.env['product.product'].sudo().search(
                                            [('name', '=', product_item)], limit=1) or False
                                        product_lot_number = "RET-" + str(source) + "-" + str(destination_code) + str(
                                            product.id)
                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', company_id.id), ('name', '=', product_lot_number)])
                                        if not lot_no:
                                            lot_number = {
                                                'name': product_lot_number,
                                                'product_id': product.id,
                                                'company_id': company_id.id
                                            }
                                            create_lot_number = request.env['stock.production.lot'].sudo().create(
                                                lot_number)
                                        lot_no = request.env['stock.production.lot'].sudo().search(
                                            [('company_id', '=', company_id.id), ('name', '=', product_lot_number)])
                                        if product:
                                            move_receipt_1 = request.env['stock.move'].sudo().create({
                                                'name': product.name,
                                                'product_id': product.id,
                                                'product_uom_qty': line["product_qty"],
                                                'quantity_done': line["product_qty"],
                                                'product_uom': product.uom_id.id,
                                                'picking_id': picking.id,
                                                'picking_type_id': picking_type.id,
                                                'location_id': location_id.id,
                                                'location_dest_id': location_dest_id.id,
                                                'company_id': company_id.id
                                            })
                                            request.env.cr.commit()
                                            move_receipt_line = request.env['stock.move.line'].sudo().search(
                                                [('move_id', '=', move_receipt_1.id)], limit=1)

                                            move_receipt_line.lot_id = lot_no.id
                                            move_receipt_line.lot_name = lot_no.name

                                picking.action_confirm()
                                picking.button_validate()

            return credit_note_no, so_numbers