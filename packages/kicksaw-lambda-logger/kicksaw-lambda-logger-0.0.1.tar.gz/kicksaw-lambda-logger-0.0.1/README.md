# kicksaw-lambda-logger

This is intended for use with Kicksaw's integration projects and our other open-source libraries like
[pycm](https://github.com/Kicksaw-Consulting/python-configuration-management). However, these aren't
hard dependencies.

# Usage

```python
from kicksaw_lambda_logger import get_logger

logger = get_logger(__name__)

logger.info("Logging is fun!")
```

# Environment variables

There are two environment variables this library makes use of:

- `STAGE`
- `LOG_LEVEL`

`STAGE` represents your deployment environment, e.g., `production`, `development`, `local`, or `test`. This affects
which logging mechanism the library uses under the hood.

`LOG_LEVEL` represents the log level, e.g., `DEBUG`, `INFO`, `WARNING`, or `ERROR`.

# Sentry

As this library grows, we'll be adding more helper methods for reporting in Sentry. For now, you can send an exception
to Sentry without your code dying by using `send_exception_to_sentry`.

# Future plans

- Write all logs to `tmp` so that other reporting tools can sweep the logs and do something with them
- Add moe Sentry features
- Pass in stage and level from outside?

---

This project uses [poetry](https://python-poetry.org/) for dependency management
and packaging.
