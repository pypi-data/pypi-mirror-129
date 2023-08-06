"""
Tests for shillelagh.fields.
"""
import datetime

from shillelagh.backends.apsw.db import connect
from shillelagh.fields import Blob
from shillelagh.fields import Boolean
from shillelagh.fields import Date
from shillelagh.fields import DateTime
from shillelagh.fields import Field
from shillelagh.fields import Float
from shillelagh.fields import IntBoolean
from shillelagh.fields import Integer
from shillelagh.fields import ISODate
from shillelagh.fields import ISODateTime
from shillelagh.fields import ISOTime
from shillelagh.fields import Order
from shillelagh.fields import String
from shillelagh.fields import StringBlob
from shillelagh.fields import StringBoolean
from shillelagh.fields import StringDuration
from shillelagh.fields import Time
from shillelagh.filters import Equal
from shillelagh.types import BINARY
from shillelagh.types import DATETIME
from shillelagh.types import NUMBER
from shillelagh.types import STRING


def test_comparison():
    """
    Test comparing fields.
    """
    field1 = Field(filters=[Equal], order=Order.ASCENDING, exact=True)
    field2 = Field(filters=[Equal], order=Order.ASCENDING, exact=True)
    field3 = Field(filters=[Equal], order=Order.ASCENDING, exact=False)

    assert field1 == field2
    assert field1 != field3
    assert field1 != 42

    assert String(filters=[Equal], order=Order.ANY, exact=True) != Integer(
        filters=[Equal],
        order=Order.ANY,
        exact=True,
    )


def test_integer():
    """
    Test ``Integer``.
    """
    assert Integer().parse(1) == 1
    assert Integer().parse(None) is None
    assert Integer().format(1) == 1
    assert Integer().format(None) is None
    assert Integer().quote("1") == "1"
    assert Integer().quote(None) == "NULL"


def test_float():
    """
    Test ``Float``.
    """
    assert Float().parse(1.0) == 1.0
    assert Float().parse(None) is None
    assert Float().format(1.0) == 1.0
    assert Float().format(None) is None
    assert Float().quote("1.0") == "1.0"
    assert Float().quote(None) == "NULL"


def test_string():
    """
    Test ``String``.
    """
    assert String().parse("1.0") == "1.0"
    assert String().parse(None) is None
    assert String().format("test") == "test"
    assert String().format(None) is None
    assert String().quote("1.0") == "'1.0'"
    assert String().quote("O'Malley's") == "'O''Malley''s'"
    assert String().quote(None) == "NULL"


def test_date():
    """
    Test ``Date``.
    """
    assert Date().parse(datetime.date(2020, 1, 1)) == datetime.date(2020, 1, 1)
    assert Date().parse(None) is None
    assert Date().format(datetime.date(2020, 1, 1)) == datetime.date(2020, 1, 1)
    assert Date().format(None) is None
    assert Date().quote(datetime.date(2020, 1, 1)) == "'2020-01-01'"
    assert Date().quote(None) == "NULL"


def test_isodate():
    """
    Test ``ISODate``.
    """
    assert ISODate().parse("2020-01-01") == datetime.date(2020, 1, 1)
    assert ISODate().parse("2020-01-01T00:00+00:00") == datetime.date(
        2020,
        1,
        1,
    )
    assert ISODate().parse(None) is None
    assert ISODate().parse("invalid") is None
    assert ISODate().format(datetime.date(2020, 1, 1)) == "2020-01-01"
    assert ISODate().format(None) is None
    assert ISODate().quote("2020-01-01") == "'2020-01-01'"
    assert ISODate().quote(None) == "NULL"


def test_time():
    """
    Test ``Time``.
    """
    assert (
        Time().parse(
            datetime.time(12, 0, tzinfo=datetime.timezone.utc),
        )
        == datetime.time(12, 0, tzinfo=datetime.timezone.utc)
    )
    assert Time().parse(None) is None
    assert (
        Time().format(
            datetime.time(12, 0, tzinfo=datetime.timezone.utc),
        )
        == datetime.time(12, 0, tzinfo=datetime.timezone.utc)
    )
    assert Time().format(None) is None
    assert (
        Time().quote(datetime.time(12, 0, tzinfo=datetime.timezone.utc))
        == "'12:00:00+00:00'"
    )
    assert Time().quote(None) == "NULL"


def test_iso_time():
    """
    Test ``ISOTime``.
    """
    assert ISOTime().parse("12:00+00:00") == datetime.time(
        12,
        0,
        tzinfo=datetime.timezone.utc,
    )
    assert ISOTime().parse("12:00") == datetime.time(
        12,
        0,
    )
    assert ISOTime().parse(None) is None
    assert ISOTime().parse("invalid") is None
    assert (
        ISOTime().format(datetime.time(12, 0, tzinfo=datetime.timezone.utc))
        == "12:00:00+00:00"
    )
    assert ISOTime().format(None) is None
    assert ISOTime().quote("12:00:00+00:00") == "'12:00:00+00:00'"
    assert ISOTime().quote(None) == "NULL"


def test_datetime():
    """
    Test ``DateTime``.
    """
    assert (
        DateTime().parse(
            datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        )
        == datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    )
    assert DateTime().parse(None) is None
    assert (
        DateTime().format(
            datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        )
        == datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    )
    assert DateTime().format(None) is None
    assert (
        DateTime().quote(
            datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        )
        == "'2020-01-01T12:00:00+00:00'"
    )
    assert DateTime().quote(None) == "NULL"


def test_iso_datetime():
    """
    Test ``ISODateTime``.
    """
    assert ISODateTime().parse("2020-01-01T12:00+00:00") == datetime.datetime(
        2020,
        1,
        1,
        12,
        0,
        0,
        tzinfo=datetime.timezone.utc,
    )
    assert ISODateTime().parse("2020-01-01T12:00") == datetime.datetime(
        2020,
        1,
        1,
        12,
        0,
        0,
    )
    assert ISODateTime().parse(None) is None
    assert ISODateTime().parse("invalid") is None
    assert (
        ISODateTime().format(
            datetime.datetime(2020, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc),
        )
        == "2020-01-01T12:00:00+00:00"
    )
    assert ISODateTime().format(None) is None
    assert (
        ISODateTime().quote("2020-01-01T12:00:00+00:00")
        == "'2020-01-01T12:00:00+00:00'"
    )
    assert ISODateTime().quote(None) == "NULL"


def test_boolean():
    """
    Test ``Boolean``.
    """
    assert Boolean().parse(True) is True
    assert Boolean().parse(False) is False
    assert Boolean().parse(None) is None
    assert Boolean().format(True) is True
    assert Boolean().format(False) is False
    assert Boolean().format(None) is None
    assert Boolean().quote(True) == "TRUE"
    assert Boolean().quote(False) == "FALSE"
    assert Boolean().quote(None) == "NULL"


def test_int_boolean():
    """
    Test ``IntBoolean``.
    """
    assert IntBoolean().parse(1) is True
    assert IntBoolean().parse(0) is False
    assert IntBoolean().parse(10) is True
    assert IntBoolean().parse(None) is None
    assert IntBoolean().format(True) == 1
    assert IntBoolean().format(False) == 0
    assert IntBoolean().format(None) is None
    assert IntBoolean().quote(1) == "1"
    assert IntBoolean().quote(0) == "0"
    assert IntBoolean().quote(None) == "NULL"


def test_string_boolean():
    """
    Test ``StringBoolean``.
    """
    assert StringBoolean().parse("TRUE") is True
    assert StringBoolean().parse("FALSE") is False
    assert StringBoolean().parse(None) is None
    assert StringBoolean().format(True) == "TRUE"
    assert StringBoolean().format(False) == "FALSE"
    assert StringBoolean().format(None) is None
    assert StringBoolean().quote("TRUE") == "TRUE"
    assert StringBoolean().quote("FALSE") == "FALSE"
    assert StringBoolean().quote(None) == "NULL"


def test_blob():
    """
    Test ``Blob``.
    """
    assert Blob().parse(b"test") == b"test"
    assert Blob().parse(None) is None
    assert Blob().format(b"test") == b"test"
    assert Blob().format(None) is None
    assert Blob().quote(b"test") == "X'74657374'"
    assert Blob().quote(None) == "NULL"


def test_string_blob():
    """
    Test ``StringBlob``.
    """
    assert StringBlob().parse("74657374") == b"test"
    assert StringBlob().parse(None) is None
    assert StringBlob().format(b"test") == "74657374"
    assert StringBlob().format(None) is None
    assert StringBlob().quote("74657374") == "X'74657374'"
    assert StringBlob().quote(None) == "NULL"


def test_type_code():
    """
    Test typecodes for Python DB API.
    """
    assert Integer == NUMBER
    assert Float == NUMBER
    assert String == STRING
    assert Date == DATETIME
    assert Time == DATETIME
    assert DateTime == DATETIME
    assert ISODate == DATETIME
    assert ISOTime == DATETIME
    assert ISODateTime == DATETIME
    assert Blob == BINARY
    assert Boolean == NUMBER

    assert NUMBER != 1


def test_string_duration():
    """
    Test ``StringDuration``.
    """
    assert StringDuration().parse("12:34:56") == datetime.timedelta(
        hours=12,
        minutes=34,
        seconds=56,
    )
    assert StringDuration().parse("12:34:56.789012") == datetime.timedelta(
        hours=12,
        minutes=34,
        seconds=56,
        microseconds=789012,
    )
    assert StringDuration().parse(None) is None
    assert StringDuration().parse("2 days, 4:00:00") == datetime.timedelta(
        days=2,
        hours=4,
    )
    assert (
        StringDuration().format(datetime.timedelta(hours=12, minutes=34, seconds=56))
        == "12:34:56"
    )
    assert (
        StringDuration().format(
            datetime.timedelta(hours=12, minutes=34, seconds=56, microseconds=789012),
        )
        == "12:34:56.789012"
    )
    assert StringDuration().format(None) is None
    assert (
        StringDuration().format(datetime.timedelta(days=2, hours=4))
        == "2 days, 4:00:00"
    )
    assert (
        StringDuration().quote(
            datetime.timedelta(hours=12, minutes=34, seconds=56, microseconds=789012),
        )
        == "'12:34:56.789012'"
    )
    assert StringDuration().quote(None) == "NULL"

    connection = connect(":memory:")
    cursor = connection.cursor()

    sql = "CREATE TABLE test_table (a DURATION)"
    cursor.execute(sql)

    sql = "INSERT INTO test_table (a) VALUES (?)"
    cursor.execute(sql, (datetime.timedelta(hours=1),))

    sql = "SELECT * FROM test_table"
    cursor.execute(sql)
    assert cursor.fetchall() == [(datetime.timedelta(hours=1),)]
