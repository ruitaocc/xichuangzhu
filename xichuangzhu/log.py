#-*- coding: UTF-8 -*-
from xichuangzhu import app
import config

# send log msg using smtp
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = (config.SMTP_USER, config.SMTP_PASSWORD)
    mail_handler = SMTPHandler((config.SMTP_SERVER, config.SMTP_PORT), config.SMTP_FROM, config.SMTP_ADMIN, 'xcz-log', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)