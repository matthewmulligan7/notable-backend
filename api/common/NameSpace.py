from flask_restx import Namespace
from flask import current_app as app

"""
Extending the flask Namespace to all for advanced add_resource
"""


class NameSpace(Namespace):

    def add_resource_with_roles(self, resource, roles, *urls, **kwargs):
        """
        Register a Resource for a given API Namespace and Register roles in app configuration

        :param Resource resource: the resource ro register
        :param list roles: A list of roles to register in app.config for the given resource path
        :param str urls: one or more url routes to match for the resource,
                         standard flask routing rules apply.
                         Any url variables will be passed to the resource method as args.
        :param str endpoint: endpoint name (defaults to :meth:`Resource.__name__.lower`
            Can be used to reference this route in :class:`fields.Url` fields
        :param list|tuple resource_class_args: args to be forwarded to the constructor of the resource.
        :param dict resource_class_kwargs: kwargs to be forwarded to the constructor of the resource.

        Additional keyword arguments not specified above will be passed as-is
        to :meth:`flask.Flask.add_url_rule`.

        Examples::

            namespace.add_resource_with_roles(HelloWorld,['user'],'/', '/hello')
            namespace.add_resource_with_roles(Foo, ['user'],'/foo', endpoint="foo")
            namespace.add_resource_with_roles(FooSpecial, ['admin'], /special/foo', endpoint="foo")
        """

        if app.config.get('POLICY') is None:
            app.config.update(dict(
                POLICY=list()
            ))

        # Extract the path if there is one
        path = self.path
        if urls is not None:
            path = "{}{}".format(self.path, urls[0])

        # Update the app.config accordingly to add a policy for the path
        app.config['POLICY'].append({"path": path, "roles": roles})

        return self.add_resource(resource, *urls, **kwargs)
