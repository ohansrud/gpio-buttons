#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

SYSTEMD_UNIT="gpio_buttons"
mv ${SYSTEMD_UNIT}.service /etc/systemd/system/
mv ${SYSTEMD_UNIT}.py /usr/local/sbin/
mv ${SYSTEMD_UNIT}_kodi /usr/local/sbin/

systemctl daemon-reload
systemctl enable ${SYSTEMD_UNIT}.service
systemctl restart ${SYSTEMD_UNIT}.service
