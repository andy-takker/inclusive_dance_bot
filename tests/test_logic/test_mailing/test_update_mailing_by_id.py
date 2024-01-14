from datetime import datetime

import pytest

from idb.db.uow import UnitOfWork
from idb.exceptions.mailing import MailingNotFoundError
from idb.logic.mailing import update_mailing_by_id

DEFAULT_DT = datetime(year=2021, month=1, day=1)


async def test_mailing_not_found(uow: UnitOfWork) -> None:
    with pytest.raises(MailingNotFoundError):
        await update_mailing_by_id(
            uow=uow,
            mailing_id=-1,
            sent_at=DEFAULT_DT,
        )
