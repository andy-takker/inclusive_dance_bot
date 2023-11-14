import asyncio
import logging

from inclusive_dance_bot.config import Settings
from inclusive_dance_bot.db.factory import create_engine, create_session_factory
from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.enums import SubmenuType
from inclusive_dance_bot.exceptions import (
    SubmenuAlreadyExistsError,
    UrlAlreadyExistsError,
    UserTypeAlreadyExistsError,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S %d.%m.%Y",
)
log = logging.getLogger(__name__)

USER_TYPES = (
    (1, "Руководитель коллектива"),
    (2, "Хореограф / педагог"),
    (3, "Специалист социокультурной сферы"),
    (4, "Танцор с ОВЗ"),
    (5, "Родитель танцора"),
    (6, "Танцующий волонтер"),
    (7, "Волонтер-организатор"),
    (8, "Зритель"),
    (9, "Партнер / благотворитель"),
    (10, "Представитель СМИ"),
    (11, "Просто интересуюсь"),
)
URLS = (
    (1, "buy_form", "https://example.com"),
    (2, "google_doc", "https://example.com"),
    (3, "ticket_timepad", "https://example.com"),
    (4, "google_form_seminar", "https://example.com"),
    (5, "buy_form_url_1", "https://example.com"),
    (6, "buy_form_url_2", "https://example.com"),
    (7, "buy_form_url_3", "https://example.com"),
    (8, "buy_form_url_4", "https://example.com"),
    (9, "buy_form_url_5", "https://example.com"),
    (10, "buy_form_url_6", "https://example.com"),
    (11, "buy_form_url_7", "https://example.com"),
    (12, "buy_form_url_8", "https://example.com"),
)
SUBMENUS = (
    (1, SubmenuType.EVENT, "Клуб професионалов Inclusive Dance", "message"),
    (
        2,
        SubmenuType.EVENT,
        "Фестиваль Inclusive Dance в Москве - октябрь 2023",
        "message",
    ),
    (3, SubmenuType.EVENT, "Социальное исследование", "message"),
    (4, SubmenuType.EDUCATION, "Клуб профессионалов Inclusive Dance", "message"),
    (5, SubmenuType.EDUCATION, "Семинары по инклюзивному танцу", "message"),
    (6, SubmenuType.EDUCATION, "Онлайн-курсы по инклюзивному танцу", "message"),
    (7, SubmenuType.ENROLL, 'Студия м. "Авимоторная" (Москва)', "message"),
    (8, SubmenuType.ENROLL, 'Студия м. "Войковская" (Москва)', "message"),
    (9, SubmenuType.CHARITY, "Сделать пожертвование", "message"),
    (10, SubmenuType.CHARITY, "Стать волонтером проекта", "message"),
    (11, SubmenuType.CHARITY, "Стать партнером проекта", "message"),
    (12, SubmenuType.CHARITY, "Рассказать о проекте", "message"),
    (13, SubmenuType.CHARITY, "Организовать показ фильма", "message"),
    (14, SubmenuType.INFORMATION, "Что такое инклюзивный танец?", "message"),
    (15, SubmenuType.INFORMATION, "О проекте Inclusive Dance?", "message"),
    (16, SubmenuType.INFORMATION, "Новости проекта", "message"),
    (
        17,
        SubmenuType.INFORMATION,
        'Документальный фильм "Танцевать под дождем"',
        "Здесь должна быть очень важная информация о фильме"
        ' и <a href="{google_doc}">ссылка</a>',
    ),
    (18, SubmenuType.INFORMATION, "Ссылки на наши ресурсы", "message"),
    (19, SubmenuType.INFORMATION, "Задать вопрос команде", "message"),
    (20, SubmenuType.OTHER, "Стать волонтером", "message"),
    (21, SubmenuType.OTHER, "Купить билет", "message"),
)


async def init_data(uow: UnitOfWork) -> None:
    log.info("Run init data")
    try:
        async with uow:
            for url in URLS:
                await uow.urls.create(slug=url[1], value=url[2], id=url[0])
            await uow.commit()
        log.info("Urls successfully initialized")
    except UrlAlreadyExistsError:
        log.warning("Urls already in database")

    try:
        async with uow:
            for user_type in USER_TYPES:
                await uow.user_types.create(id=user_type[0], name=user_type[1])
            await uow.commit()
        log.info("UserTypes successfully initialized")
    except UserTypeAlreadyExistsError:
        log.warning("UserTypes already in database")

    try:
        async with uow:
            for submenu in SUBMENUS:
                await uow.submenus.create(
                    id=submenu[0],
                    type=submenu[1],
                    button_text=submenu[2],
                    message=submenu[3],
                )
            await uow.commit()
        log.info("Submenu successfully initialized")
    except SubmenuAlreadyExistsError:
        log.warning("Submenu already in database")
    log.info("Finish init data")


def main() -> None:
    settings = Settings()
    engine = create_engine(connection_uri=settings.build_db_connection_uri())
    session_factory = create_session_factory(engine=engine)
    uow = UnitOfWork(sessionmaker=session_factory)
    asyncio.run(init_data(uow=uow))


if __name__ == "__main__":
    main()
