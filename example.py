from xweb import App

from xweb_router import Router

app = App()
router = Router()
nested = Router()

app.use(router)


@router.use('/')
async def middleware(ctx, fn):
    """Router Middleware"""
    print('middleware')
    await fn()


@router.post('/')
async def home(ctx):
    ctx.body = "Home"


@router.get('/{name}')
async def hello(ctx):
    """URL parameters"""
    ctx.body = f"Hello {ctx.params.name}"


@nested.get('/index')
async def index(ctx):
    """Nest Router"""
    ctx.body = "Nested Index"


router.use('/post')(nested)

if __name__ == '__main__':
    app.listen(8000)
