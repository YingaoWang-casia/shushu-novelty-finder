"""Stable public errors and CLI exit codes."""


class ShushuError(Exception):
    """Base class for expected workflow failures."""


class InputError(ShushuError):
    """The user-supplied file or argument is invalid."""


class RetrievalError(ShushuError):
    """A retrieval source failed or returned invalid data."""


class GateError(ShushuError):
    """A workflow artifact failed its phase gate."""


EXIT_OK = 0
EXIT_INVALID_INPUT = 2
EXIT_RETRIEVAL_FAILURE = 3
EXIT_GATE_FAILURE = 4
