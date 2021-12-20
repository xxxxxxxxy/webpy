import web
render = web.template.render('templates/')
urls = (
    '/', 'index',
    '/showmeme', 'showmeme'
)

class index:
    def GET(self):
        name = 'Bob'    
        return render.test(name)

class showmeme:
    def GET(self):
        return render.image()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()