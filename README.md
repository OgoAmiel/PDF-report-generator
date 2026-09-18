# PDF Report Generator

Daily idempotency prevents repeated requests from creating duplicate reports and wasting rendering resources. Without this check, a retry of an email-report request could send the same customer the same report twice.

Move report generation to a background job when rendering becomes slow enough to exceed a user-facing request timeout or needs reliable retries.