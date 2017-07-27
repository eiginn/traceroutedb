from geoip2.errors import AddressNotFoundError


def ip_asn(app, ip):
    try:
        reader = app.config.get("trdb").get("mmdb")
    except:
        return None

    try:
        ret = reader.isp(ip)
    except AddressNotFoundError:
        return None

    return ret
