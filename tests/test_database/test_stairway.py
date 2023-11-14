from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory


def get_revisions(alembic_config: Config) -> list[Script]:
    revisions_dir = ScriptDirectory.from_config(alembic_config)
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


def test_migrations_stairway(alembic_config, subtests):
    for revision in get_revisions(alembic_config):
        with subtests.test(msg="revision", revision=revision):
            upgrade(alembic_config, revision.revision)
            downgrade(alembic_config, revision.down_revision or "-1")
            upgrade(alembic_config, revision.revision)
