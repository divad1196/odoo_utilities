# -*- coding: utf-8 -*-


import base64

def action_edit_attachment(env, content, attachment_xml_id):
    """
        Rewrite an existing attachment and return the download action

        env: odoo env, can be retrieve using self.env
        content: content of the file (not encoded)
        attachment_xml_id: the xml_id of the attachment where to store the data
    """
    if not content:
        raise UserError(_('Could not generate CSV file'))
    attachment = env.ref(attachment_xml_id, None)
    if not attachment:
        raise UserError(_('Could not find default attachement for this report'))
    attachment.write({
        'datas': base64.b64encode(content)
    })
    return {
        'type': 'ir.actions.act_url',
        'target': 'self',
        'url': '/web/content/{id}/{filename}?download=true'.format(
            id=attachment.id,
            filename=attachment.name
        )
    }

def action_create_attachment(attach_record, file_name, content):
    """
        Create an attachment and return the download action

        attach_record: Record to which to attach the attachment
        file_name: name of the file
        content: content of the file (not encoded)
    """
    if not (attach_record and file_name and content):
        raise UserError(_('Could not generate CSV file'))

    attach_record.ensure_one()
    attachment_id = attach_record.env['ir.attachment'].create({
        'name': file_name,
        'datas_fname': file_name,
        'type': 'binary',
        'datas': base64.b64encode(content),
        'res_model': attach_record._name,
        'res_id': attach_record.id,
    })
    
    return {
        'type': 'ir.actions.act_url',
        'target': 'self',
        'url': '/web/content/{id}/{filename}?download=true'.format(
            id=attachment.id,
            filename=attachment_id.name
        )
    }
