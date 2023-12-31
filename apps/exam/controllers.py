"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from py4web.utils.form import Form
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from pydal.restapi import Policy, RestAPI

policy = Policy()
policy.set("exam", "GET", authorize=True)
policy.set("exam", "POST", authorize=True)
#policy.set(db.exams, "PUT", authorize=True)

@action("index", method=["POST", "GET"])
@action.uses("index.html", auth.user, T, db)
def index():
    form = Form(db.exam)
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = {"allowed_actions": auth.param.allowed_actions}
    return dict(message=message, actions=actions, form=form)

@action("profile", method=["POST", "GET"])
@action.uses("index.html", auth.user, T, db)
def index():
    form = Form(db.profile)
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = {"allowed_actions": auth.param.allowed_actions}
    return dict(message=message, actions=actions, form=form)

@action("api/<table>", method=["POST", "GET"])
@action("api/<table>/<rec>", method=["GET", "PUT", "DELETE"])
@action.uses(db)
def api(table, rec=None):
    return RestAPI(db, policy)(
        request.method,
        table,
        rec,
        request.GET,
        request.POST
    )
