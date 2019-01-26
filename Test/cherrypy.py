import cherrypy

class View(object):
	@cherrypy.expose
	def index(self):
		return "Hello World! View"

class Post(object):
	@cherrypy.expose
	def index(self):
		return \
"""
<form action=\"answer\" method=\"post\">
<input type=numeric name="val1"/>
<input type=numeric name="val2"/>
<input type=submit value="envoyer"/>
</form>
"""

	@cherrypy.expose
	def answer(self, val1, val2):
		return str(int(val1) + int(val2))

cherrypy.tree.mount(View(), '/view')
cherrypy.tree.mount(Post(), '/post')

cherrypy.engine.start()
cherrypy.engine.block()
