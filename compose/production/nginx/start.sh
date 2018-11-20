#!/bin/bash

echo "Starting Nginx"
nginx
tail -f /var/log/nginx/*.log
