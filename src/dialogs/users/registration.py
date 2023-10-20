from aiogram_dialog import Dialog

from src.dialogs.users.messages import (
    INPUT_NAME_MESSAGE,
    INPUT_PHONE_NUMBER_MESSAGE,
    INPUT_REGION_MESSAGE,
)
from src.dialogs.users.windows.choose_user_types import ChooseUserTypesWindow
from src.dialogs.users.windows.confirm import ConfirmWindow
from src.dialogs.utils.input_form_field import InputFormWindow
from src.states import RegistrationSG


class RegistrationDialog(Dialog):
    def __init__(self) -> None:
        super().__init__(
            InputFormWindow(
                state=RegistrationSG.input_name,
                field_name="name",
                message=INPUT_NAME_MESSAGE,
                is_first=True,
            ),
            ChooseUserTypesWindow(
                state=RegistrationSG.choose_types,
            ),
            InputFormWindow(
                state=RegistrationSG.input_place,
                field_name="region",
                message=INPUT_REGION_MESSAGE,
            ),
            InputFormWindow(
                state=RegistrationSG.input_phone_number,
                field_name="phone_number",
                message=INPUT_PHONE_NUMBER_MESSAGE,
            ),
            ConfirmWindow(state=RegistrationSG.confirm),
        )
