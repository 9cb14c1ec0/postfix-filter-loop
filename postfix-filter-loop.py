#!/usr/bin/python3
# Author: Miroslav Houdek miroslav.houdek at gmail dot com
# License is, do whatever you wanna do with it (at least I think that that is what LGPL v3 says)
#

import smtpd
import asyncore
import smtplib
import traceback


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):

        try:
            # DO WHAT YOU WANNA DO WITH THE EMAIL HERE
            # In future I'd like to include some more functions for users convenience,
            # such as functions to change fields within the body (From, Reply-to etc),
            # and/or to send error codes/mails back to Postfix.
            # Error handling is not really fantastic either.
            with open('/opt/postfix-filter-loop/msg.txt', 'w') as f:
                f.write(data)

        except:
            print('Something went south')
            print(traceback.format_exc())

        try:
            server = smtplib.SMTP('localhost', 10032)
            server.sendmail(mailfrom, rcpttos, data)
            server.quit()
        except smtplib.SMTPException:
            print('Exception SMTPException')
            pass
        except smtplib.SMTPServerDisconnected:
            print('Exception SMTPServerDisconnected')
            pass
        except smtplib.SMTPResponseException:
            print('Exception SMTPResponseException')
            pass
        except smtplib.SMTPSenderRefused:
            print('Exception SMTPSenderRefused')
            pass
        except smtplib.SMTPRecipientsRefused:
            print('Exception SMTPRecipientsRefused')
            pass
        except smtplib.SMTPDataError:
            print('Exception SMTPDataError')
            pass
        except smtplib.SMTPConnectError:
            print('Exception SMTPConnectError')
            pass
        except smtplib.SMTPHeloError:
            print('Exception SMTPHeloError')
            pass
        except smtplib.SMTPAuthenticationError:
            print('Exception SMTPAuthenticationError')
            pass
        except:
            print('Undefined exception')
            print(traceback.format_exc())

        return


server = CustomSMTPServer(('127.0.0.1', 10031), None)

asyncore.loop()
