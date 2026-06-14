FROM alpine:3.24
WORKDIR /src
COPY . .
LABEL org.opencontainers.image.source="https://github.com/mafzalkalwardev/python-auto-dialer-pro"
CMD ["sh", "-c", "echo 'python-auto-dialer-pro source package' && ls -1"]
