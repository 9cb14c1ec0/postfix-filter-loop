postfix-filter-loop
===================

This is a very simple Python code to achieve Advanced Content Filtering in 
Postfix ( http://www.postfix.org/FILTER_README.html ) . This Python code 
listens on one port to get emails from Postfix, then you can do the magic 
(remove email, change contents) and then re-inject the mail into Postfix. 
I needed a Python code to do just that, using only standard modules, and 
absolutely straightforward. So there, get it, configure Postfix, start it, 
and do whatever you want with headers or body.

##Installation
To install, run these commands as root.
```commandline
git clone https://github.com/9cb14c1ec0/postfix-filter-loop
python3 postfix-filter-loop/install.py
```

Now, you need to configure Postfix. Edit configuration according to the 
suggestions made in the Advanced Content Filtering above, but for your 
convenience, here is the quick version that could work for you too:

`/etc/postfix/main.cf`:
```
content_filter = scan:localhost:10031
receive_override_options = no_address_mappings
```

`/etc/postfix/master.cf`:
```
scan      unix  -       -       n       -       10      smtp
      -o smtp_send_xforward_command=yes
      -o disable_mime_output_conversion=yes

localhost:10032 inet  n       -       n       -       10      smtpd
      -o content_filter=
      -o receive_override_options=no_unknown_recipient_checks,no_header_body_checks,no_milters
      -o smtpd_authorized_xforward_hosts=127.0.0.0/8
```

There are many combinations of parameters that could work, (see the FILTER_README referred 
above) but only this one worked for me. This is because what I needed is that mails 
come to my Python code BEFORE processed using virtual table and they get processed 
using virtual table AFTER. This is what I needed, but you can change the 
no_address_mappings parameter in main.cf and master.cf to do thy bidding.

## iRedMail installation

Add these lines to master.cf:

```commandline
# postfix-filter-loop integration
postfix-filter-loop unix -  -   n   -   2  smtp
    -o syslog_name=postfix/postfix-filter-loop
    -o smtp_data_done_timeout=1200
    -o smtp_send_xforward_command=yes
    -o disable_dns_lookups=yes
    -o max_use=20

# smtp port used by postfix-filter-loop to re-inject processed email
# back to Postfix
127.0.0.1:10032 inet n  -   n   -   - smtpd
    -o syslog_name=postfix/10032
    -o content_filter=
    -o mynetworks_style=host
    -o mynetworks=127.0.0.0/8
    -o local_recipient_maps=
    -o relay_recipient_maps=
    -o strict_rfc821_envelopes=yes
    -o smtp_tls_security_level=none
    -o smtpd_tls_security_level=none
    -o smtpd_restriction_classes=
    -o smtpd_delay_reject=no
    -o smtpd_client_restrictions=permit_mynetworks,reject
    -o smtpd_helo_restrictions=
    -o smtpd_sender_restrictions=
    -o smtpd_recipient_restrictions=permit_mynetworks,reject
    -o smtpd_end_of_data_restrictions=
    -o smtpd_error_sleep_time=0
    -o smtpd_soft_error_limit=1001
    -o smtpd_hard_error_limit=1000
    -o smtpd_client_connection_count_limit=0
    -o smtpd_client_connection_rate_limit=0
    -o receive_override_options=no_header_body_checks,no_unknown_recipient_checks,no_address_mappings
```

Then scroll down to these lines:
```commandline
# smtp port used by Amavisd to re-inject scanned email back to Postfix
127.0.0.1:10025 inet n  -   n   -   -  smtpd
    -o syslog_name=postfix/10025
    -o content_filter=

```

And change them to this:
```commandline
# smtp port used by Amavisd to re-inject scanned email back to Postfix
127.0.0.1:10025 inet n  -   n   -   -  smtpd
    -o syslog_name=postfix/10025
    -o content_filter=postfix-filter-loop:[127.0.0.1]:10031

```
There are very good alternatives to using my code - specifically FuGlu 
( http://www.fuglu.org/ ) - which I did not want to use because it is a bit more 
complex than I needed, and also seems to just have emphasis on filtering, whereas 
what I wanted to do was not only filter, but also change the content of mails. There 
is also Perl code which (I think) is similar SMTPProx http://bent.latency.net/smtpprox/ 
but I don't know Perl by heart and I suspected that the code would again be more 
complicated to bend to my purposes.

