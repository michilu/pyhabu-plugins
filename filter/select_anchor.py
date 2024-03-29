from StringIO import StringIO
import habu.log as log

try:
    from lxml import etree
    _PARSING_MODULE = "lxml"
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
        _PARSING_MODULE = "BeautifulSoup"
    except ImportError:
        raise Warning('ImportError. Required lxml(http://codespeak.net/lxml/) or BeautifulSoup(http://www.crummy.com/software/BeautifulSoup/).')


class Main(object):
    def __init__(self, config, environ):
        pass

    def execute(self, context):
        items = list()
        for entry in context["entries"]:
            for url, title in get_links(entry).items():
                items.append(dict(
                    link = url,
                    title = title,
                    updated = entry.get("updated"),
                    updated_parsed = entry.get("updated_parsed"),
                ))
        context["entries"] = items
        return context


def create(*argv, **kwargv):
    return Main(*argv, **kwargv)

def get_links(*argv, **kwargv):
    links = dict(
        lxml = _l_get_links,
        BeautifulSoup = _b_get_links,
    ).get(_PARSING_MODULE)(*argv, **kwargv)
    log.info(u"Selected %d anchor(s)" % len(links))
    return links

def _l_get_links(entry):
    links = dict()
    parser = etree.HTMLParser()
    for href in etree.parse(StringIO(entry["summary"]), parser).xpath("//*[@href]"):
        links.update({u"%s" % href.attrib.get("href"): href.text})
        #log.debug(href.attrib.get("href"), href.text.encode("utf-8"))
    return links

def _b_get_links(entry):
    links = dict()
    for href in BeautifulSoup(entry["summary"]).findAll("a"):
        links.update({u"%s" % href.get("href"): unicode(href.string)})
        #log.debug(href.attrib.get("href"), href.text.encode("utf-8"))
    return links
