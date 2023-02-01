#!/bin/bash

#Coloring
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Set the script to exit immediately if any commands return an error code
set -e

echo "Started script at $(date)"

mkdir certs;cd certs

echo -e "${GREEN}" "GENERATING ROOT CA KEY AND CERTIFICATE..."
echo -e "${NC}" 
openssl genrsa -out rootCA.key 4096
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem -subj "/C=US/ST=WA/O=Microsoft/CN=MyAwesomeRootCA"

echo -e "${GREEN}" "GENERATING DEVICE KEY AND A CSR..."
echo -e "${NC}" 
openssl genrsa -out device1.key 2048
openssl req -new -sha256 -key device1.key -subj "/C=US/ST=WA/O=Microsoft/CN=device1" -out device1.csr
openssl req -in device1.csr -noout -text

echo -e "${GREEN}" "GENERATING A DEVICE CERTIFICATE..."
echo -e "${NC}" 
openssl x509 -req -in device1.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device1.pem -days 500 -sha256
openssl x509 -in device1.pem -text -noout

echo -e "${GREEN}" "SCRIPT COMPLETED SUCCESSFULLY!"
echo -e "${NC}" 
