from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp

from routes.courses import router as course_router
from routes.enrollments import router as enroll_router
from routes.payments import router as payment_router

import notifications
from graphql_api import schema

app = FastAPI()

# REST APIs
app.include_router(course_router)
app.include_router(enroll_router)
app.include_router(payment_router)

# GraphQL
app.add_route("/graphql", GraphQLApp(schema))
