
import cherrypy
from infosecbot.storage import storage
from html import escape
	  
class LinkController(object):
    def link_to_html(self, link):
        return """<div>
            <a href="%s">%s (%d)</a>
            <form method="POST" action="vote">
                <input type="submit" name="rate" value="+1">
                <input type="submit" name="rate" value="-1">
                <input type="hidden" name="link_id" value="%s">
            </form>
            </div>""" % (escape(link.url), escape(link.title), link.score, escape(link.id))
        
    @cherrypy.expose
    def index(self):
        response = ""
        for link in storage['links']:
            response += self.link_to_html(link)
        return response

    @cherrypy.expose
    def vote(self, link_id, rate):
        link = storage.get_link(link_id)
        link.score += int(rate)
        storage.save()
        raise cherrypy.HTTPRedirect("/")

cherrypy.quickstart(LinkController())
