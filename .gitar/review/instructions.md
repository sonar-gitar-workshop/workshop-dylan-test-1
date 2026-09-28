# Customer-facing order references

In addition to standard code review, enforce this convention for every new or
changed customer-facing order reference in `app.py`:

- Use `ORDER-` followed by the numeric order ID padded to six digits.
- For example, order ID `1` must be rendered as `ORDER-000001`.

Report a blocking review finding whenever a changed order response exposes a
reference that does not follow this format, even when the endpoint works and
its tests pass.

Do not suppress, replace, or downgrade standard reliability, security, or
maintainability findings when applying this convention.
