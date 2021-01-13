import uuid
import pytest
from quetz.db_models import User, Profile

pytest_plugins = "quetz.testing.fixtures"

@pytest.fixture
def plugins():
    # defines plugins to enable for testing
    return ['quetz-{{cookiecutter.plugin_name}}']

@pytest.fixture
def jobs_user(db):

    user = User(id=uuid.uuid4().bytes, username="jobs_user", role="maintainer")
    profile = Profile(user=user, avatar_url="http://my-avatar")
    db.add(user)
    db.add(profile)
    db.commit()

    return user
