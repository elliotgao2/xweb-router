# xweb-router

> Router middleware for [xweb](https://github.com/gaojiuli/xweb)


## Usage

```python
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


router.use('/post')(nested)


@nested.get('/index')
async def index(ctx):
    ctx.body = "Nested Index"


if __name__ == '__main__':
    app.listen(8000)

```

## Nested Router

```python

```