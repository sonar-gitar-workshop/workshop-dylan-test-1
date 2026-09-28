# Gitar workshop

A hands-on workshop where you fork a small Flask order service, connect [Gitar](https://gitar.ai), and open pull requests that show how Gitar reviews code, enforces project conventions, diagnoses a CI failure, and fixes it.

Three pre-staged branches keep each application change small, so every diff is short and readable on screen. Everything happens in the browser.

## Part 1: Setup

### Fork the repository

1. On the [sonar-samples/gitar-workshop](https://github.com/sonar-samples/gitar-workshop) page, click **Fork**.
2. Leave **Copy the `main` branch only** unchecked so the workshop branches come along with their shared history.
3. Create the fork.

### Enable CI

1. In your fork, go to **Actions** and enable workflows if prompted.
2. Open the **Test** workflow and click **Run workflow** on the `main` branch. Wait for it to pass. This registers the `test` check so branch protection can require it later.

### Connect Gitar

1. In Gitar, open **Settings > Configuration** and connect your GitHub account if it is not already connected.
2. Grant Gitar access to your fork.
3. Return to **Settings > Configuration** and confirm that the fork is connected.

### Configure merge controls

1. In your fork's **Settings > General**, scroll to **Pull Requests** and enable **Allow auto-merge**.
2. Under **Settings > Rules > Rulesets**, create an active branch ruleset that targets `main`, requires pull requests, requires one approval, and requires the `test` status check to pass before merging.

### Confirm Gitar settings

In Gitar, confirm that auto-approve is enabled for your repository. Auto-apply and auto-merge should both be off because Part 4 enables them for a single PR.

## Part 2: Business logic review

Open a pull request with **base** `main` and **compare** `part-2-price-override`.

Before creating it, read the diff. The change lets API clients submit their own `unit_price_cents` while a comment at the top of `app.py` says catalog prices are authoritative.

Create the pull request and wait for Gitar's review.

When the review appears, read the findings and the proposed fix. Then comment:

```text
gitar fix this
```

After the fix commit lands, inspect the diff to confirm the catalog is still treated as authoritative, then check that CI is green. Gitar may leave a separate finding, such as missing test coverage, for you to consider. Leave this PR open.

## Part 3: Repository-specific context

Open a pull request with **base** `main` and **compare** `part-3-context-ingestion`.

This branch adds two configuration files alongside a code change:

- `.gitar/review/instructions.md` defines a naming convention for order references (the `ORDER-000001` format).
- `.gitar/rules/order-api-change-check.md` requests API documentation updates whenever `app.py` changes.

The code change adds a `reference` field that violates the instruction's naming convention.

When the review lands, look for the convention-based finding, the separate rule action, and the `documentation` label. Do not request a fix for this PR.

## Part 4: CI failure and automated remediation

Open a pull request with **base** `main` and **compare** `part-4-ci-failure`.

The branch changes the response for unknown products from HTTP 404 to HTTP 200, which breaks a test that asserts the original status code. Wait for CI to fail.

Gitar posts a diagnosis of the failure on the PR. Read it before doing anything else because it may not remain visible after remediation.

Post one comment with both controls:

```text
gitar auto-apply:on
gitar auto-merge:on
```

Gitar commits a fix to the branch. GitHub reruns CI against the new commit and waits for the required check and approval before merging.

Verify the fix by reading the commit diff and confirming that CI passes.

## Part 5: Functional validation

Enable github issue features on the [setting page](/../../settings)

Create a new issue as follows:
```text
Title: [Feature request] Create a delete order endpoint
Description:
Add the ability to delete an order with the following requirement:
- Required order ID, SKU and quantity field
- If no order ID is found, return a 500 error
- If the order ID is found, but the SKU is not found, return a 500 error
- If the quantity field exceeds the current quantity, return a JSON error
- Once completed, return the order ID, SKU, remaining SKU quantity, and updated total
```

Open a new pull request with **base** `main` and **compare** `part-5-functional-validation` and make sure the newly created issue above is linked to the same pull request.

To link an issue to a pull request in Github. Add this description in the pull request
```text
This pull request is created to implement this issue #<num>

Closing this will resolve #<num>
```

The branch will try to implement the above feature. Gitar will check if the requirements are met with the new implementation.

Verify the implementation.

## Troubleshooting

**No review appears.** Confirm the repository is connected in Gitar and that you have a Gitar seat. You can comment `gitar review` to request a re-review.

**No workflow run.** Make sure you enabled Actions and ran the Test workflow manually during setup.

**Part 4 merges before you read the diagnosis.** Auto-apply or auto-merge was enabled before the exercise. Both should be off until you post the comment.

## Resources

- [Gitar documentation](https://docs.gitar.ai)
- [Commands reference](https://docs.gitar.ai/commands)
- [CI failure analysis](https://docs.gitar.ai/features/ci-failure-analysis)
- [Repository rules](https://docs.gitar.ai/features/rules)
- [Auto-merge](https://docs.gitar.ai/features/code-review/auto-merge)
