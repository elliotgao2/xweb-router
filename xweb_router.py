from collections import defaultdict
from functools import partial
from inspect import signature

import parse
from xweb import HTTPException, HTTPStatus

__version__ = '0.1.0'
__author__ = 'Jiuli Gao'
__all__ = ('Router',)


class Router:
    def __init__(self):
        self.routes = defaultdict(list)

    async def __call__(self, ctx, fn):
        for path, handlers in self.routes.items():
            parse_result = parse.parse(path, ctx.req.url)
            if parse_result is None:
                continue
            ctx.params = parse_result.named
            next_fn = None
            for handler in handlers[::-1]:
                if len(signature(handler).parameters) == 2:
                    next_fn = partial(handler, ctx=ctx, fn=next_fn)
                else:
                    next_fn = partial(handler, ctx=ctx)
            try:
                await next_fn()
                if fn:
                    await fn()
                return
            except HTTPException as e:
                ctx.res.status = e.status
                ctx.res.body = e.msg or HTTPStatus(e.status).phrase
                ctx.res.msg = e.properties
        ctx.abort(404)

    def use(self, path):
        def callback(fn):
            self.routes[path].append(fn)

        return callback

    def get(self, path):
        return self.use(path)

    def put(self, path):
        return self.use(path)

    def post(self, path):
        return self.use(path)

    def patch(self, path):
        return self.use(path)

    def delete(self, path):
        return self.use(path)
