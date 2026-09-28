---
title: "Order API documentation"
description: "Flag undocumented changes to public order responses"
when: "A pull request is opened or updated and changes app.py"
actions: "When a Flask JSON response changes, add the existing documentation label and post a pull request comment requesting an API-contract documentation update"
---

# Documentation required for order API changes

Review changes to `app.py` for JSON responses returned by public Flask route
handlers.

When a response adds, removes, or renames a field:

- Add the existing `documentation` label to the pull request.
- Post a pull request comment headed `Order API documentation required` that
  identifies the changed response and asks for its API-contract documentation
  to be updated before merge.

Do not apply the label or post a comment for an internal refactor that leaves
the JSON response unchanged. Do not modify application code.
