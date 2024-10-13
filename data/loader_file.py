from aiogram.types import FSInputFile


def load_file(category: str, filename: str, alter_filename: str = None) -> FSInputFile:
    """Функция по загрузке файлов"""

    if alter_filename:
        name = alter_filename
    else:
        name = filename

    return FSInputFile(
        path=f'data/{category}/{filename}',
        filename=name
    )
