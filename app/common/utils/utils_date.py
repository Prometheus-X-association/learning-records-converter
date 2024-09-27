import dateparser


def parse_date(
    date: str | int,
    date_format: str | None = None,
    user_locale: str | None = None,
) -> str | None:
    """
    Parse and format a date string to ISO 8601 format.

    This function uses the dateparser library to parse various date formats
    and convert them to ISO 8601 format in UTC. It supports custom date formats
    and locales for more accurate parsing.

    :param date: The date to be parsed
    :param date_format: Optional custom date format to use for parsing
    :param user_locale: Optional locale to use for parsing (e.g., 'fr' for French)
    :return: The parsed date in ISO 8601 format, or None if parsing fails
    """

    try:
        locales = [user_locale] if user_locale else None
        date_formats = [date_format] if date_format else None

        parsed_date = dateparser.parse(
            date_string=str(date),
            locales=locales,
            date_formats=date_formats,
            settings={
                "TIMEZONE": "UTC",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DAY_OF_MONTH": "first",
                "PREFER_MONTH_OF_YEAR": "first",
                "PREFER_DATES_FROM": "past",
            },
        )
        return parsed_date.isoformat() if parsed_date is not None else parsed_date
    except (ValueError, TypeError):
        return date
