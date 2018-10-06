# xweb-router

> Router middleware for [xweb](https://github.com/gaojiuli/xweb)

```python
from xweb import App

from xweb_router import Router

app = App()
router = Router()

app.use(router)


@router.use('/')
async def xxx(ctx, fn):
    print('middleware')
    await fn()


@router.get('/')
async def hello(ctx):
    ctx.body = "Hello World!"


@router.post('/home')
async def home(ctx):
    ctx.body = "Home"


@router.patch('/index')
async def index(ctx):
    ctx.body = "Index"


if __name__ == '__main__':
    app.listen(8000)
```