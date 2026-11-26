# OpenCondo’s missing-variable test failed because it inherited a setting

OpenCondo supports property management, resident requests, billing and service workflows. The audit recorded **one confirmed test-fixture defect**. The audited run also captured selected package checks and a prepared service smoke test.

## Confirmed finding

**F1 · Environment isolation in the missing-variable test.** The fixture left `REDIS_URL` out of its app environment file, but the test process already had the setting. The implementation returned the configured global fallback. The fixture expected an absent value and falsely failed. Separate tests for global fallback and app-file precedence passed. Isolate the missing-variable fixture from inherited settings, then rerun it alongside both controls. Evidence E4, E27 and E28.

## What was verified

| Check | What the audit observed |
| --- | --- |
| Prepared Linux startup | Keystone initialized, and read/write smoke checks passed against disposable PostgreSQL and Redis services. Evidence E3. |
| Global fallback and app-file precedence | The recorded package tests returned the global value when the app file omitted it and used the app-file value when both were present. Evidence E4, E27 and E28. |
| Sample ticket URL | The recorded package case accepted the expected sample application URL. Evidence E4 and E21. |

## Coverage limits

The as-shipped Node entry reached its 12-second observation limit. The billing suite stopped at a build-hook failure before any payment-split assertion, and other suites had missing prerequisites or timeouts. The prepared service checks establish startup and connectivity in that environment. End-to-end property management, payments and integrations remain unverified. Evidence E2, E3, E4, E32 and E71.

## Audit record

The saved report was sealed on November 25, 2026. Snapshot SHA-256 `34bbe88ad7b2f09fdec43ef875320b326fb8627393a9b7318b9b4c8ad2a2d77b`. [Audited OpenCondo revision](https://github.com/open-condo-software/condo/tree/a9358a545377764b445c6e0c68fb517567c27c8d) · [All audited repositories](README.md#audited-repositories)
