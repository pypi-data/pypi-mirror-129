<img width="350px" src="https://storage.googleapis.com/nectar-mosaic-public/images/kama/services/lets_encrypt/banner.png"/>

<br/>
<br/>

The ACME Issuer type represents a single account registered with the Automated Certificate Management Environment (ACME) Certificate Authority server. When you create a new ACME Issuer, cert-manager will generate a private key which is used to identify you with the ACME server.

Certificates issued by public ACME servers are typically trusted by client’s computers by default. This means that, for example, visiting a website that is backed by an ACME certificate issued for that URL, will be trusted by default by most client’s web browsers. ACME certificates are typically free.

## Solving Challenges

In order for the ACME CA server to verify that a client owns the domain, or domains, a certificate is being requested for, the client must complete “challenges”. This is to ensure clients are unable to request certificates for domains they do not own and as a result, fraudulently impersonate another’s site. As detailed in the RFC8555, cert-manager offers two challenge validations - HTTP01 and DNS01 challenges.

HTTP01 challenges are completed by presenting a computed key, that should be present at a HTTP URL endpoint and is routable over the internet. This URL will use the domain name requested for the certificate. Once the ACME server is able to get this key from this URL over the internet, the ACME server can validate you are the owner of this domain. When a HTTP01 challenge is created, cert-manager will automatically configure your cluster ingress to route traffic for this URL to a small web server that presents this key.

DNS01 challenges are completed by providing a computed key that is present at a DNS TXT record. Once this TXT record has been propagated across the internet, the ACME server can successfully retrieve this key via a DNS lookup and can validate that the client owns the domain for the requested certificate. With the correct permissions, cert-manager will automatically present this TXT record for your given DNS provider.




## Use an Alternative Certificate Chain


On January 11th 2021, Let’s Encrypt will change over to using its own ISRG Root CA. This will replace the cross-signed certificates by Identrust. This change over needs no changes to your cert-manager configuration, any renewed or new certificates issued after this date will use the new CA root.

Let’s encrypt currently already signs certificates using this CA and offers them as “alternative certificate chain” via ACME. In this release cert-manager adds support for accessing these alternative chains in the issuer config. The new preferredChain option will allow you to specify a CA’s common name for the certificate to be issued by. If there is a certificate available matching that request it will present you that certificate. Note that this is a Preferred option, if none is found matching the request it will give you the default certificate as before. This makes sure you still get your certificate renewed once the alternative chain gets removed on the ACME issuer side.

You can already today get certificates from the ISRG Root by using: