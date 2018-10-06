from collections import defaultdict
from functools import partial
from inspect import signature

import parse

__version__ = '0.1.1'
__author__ = 'Jiuli Gao'
__all__ = ('Router',)


class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class Router:
    def __init__(self, prefix=''):
        self.prefix = prefix
        self.routes = defaultdict(list)

    async def __call__(self, ctx, fn=None):
        for path, handlers in self.routes.items():
            parse_result = parse.parse(path, ctx.req.url)
            if parse_result is None:
                continue
            ctx.params = AttributeDict()
            ctx.params.update(parse_result.named)
            next_fn = None
            route_defined = False
            for handler in handlers[::-1]:
                if handler['method'] is not None and handler['method'] != ctx.req.method:
                    continue
                if len(signature(handler['fn']).parameters) == 2:
                    if isinstance(handler['fn'], Router):
                        route_defined = True
                    next_fn = partial(handler['fn'], ctx=ctx, fn=next_fn)
                else:
                    route_defined = True
                    next_fn = partial(handler['fn'], ctx=ctx)
            if not route_defined:
                ctx.abort(405)
            await next_fn()
            if fn:
                await fn()
            return
        ctx.abort(404)

    def use(self, path, method=None):
        def callback(fn):
            if isinstance(fn, Router):
                fn.prefix = path
                self.routes[self.prefix + path + '{}'].append({'fn': fn, 'method': method})
            else:
                self.routes[self.prefix + path].append({'fn': fn, 'method': method})

        return callback

    def get(self, path):
        return self.use(path, 'GET')

    def put(self, path):
        return self.use(path, 'PUT')

    def post(self, path):
        return self.use(path, 'POST')

    def patch(self, path):
        return self.use(path, 'PATCH')

    def delete(self, path):
        return self.use(path, 'DELETE')
