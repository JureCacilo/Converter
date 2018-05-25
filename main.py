#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class ConvertHandler(BaseHandler):
    def post(self):
       dolzina = float(self.request.get("dolzina"))
       kolicina = self.request.get("kolicina")

       pretvorjena_dolzina = 0
       nova_kolicina = None
       pretvornik = 1.6
       if kolicina == "milje":
           pretvorjena_dolzina = dolzina / pretvornik
           nova_kolicina = "km"
        
       elif kolicina == "km":
            pretvorjena_dolzina = dolzina * pretvornik
            nova_kolicina = "milje"
        
        

        

        

       params = {"dolzina": dolzina, "kolicina": kolicina, "pretvorjena_dolzina": pretvorjena_dolzina, "nova_kolicina": nova_kolicina}

       return self.render_template("pretvori.html", params = params)
        



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/pretvori', ConvertHandler),
], debug=True)
