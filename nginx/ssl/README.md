# Directory for TLS certificates and keys

Place your TLS (Transport Layer Security) certificates and private keys for NGINX in this directory. These files are essential for enabling HTTPS, ensuring secure communication, and authenticating server identity. Make sure use correct certificate/private key pair for the domain you are running the studio on.

   - Certificates (.crt or .pem): Store public certificates issued by a Certificate Authority (CA) here.
   - Private Keys (.key): Store corresponding private keys securely here.

Ensure correct file permissions to maintain security and limit access to sensitive key files:
   - Certificate files (.pem): should be readable (644)
   - Private key files: should be restricted (600)
