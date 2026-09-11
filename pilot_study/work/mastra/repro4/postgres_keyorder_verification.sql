-- Direct verification against a real PostgreSQL 16 instance (Docker) that
-- jsonb columns genuinely reorder object keys on round-trip, while text
-- columns preserve insertion order -- confirming the mechanism
-- mastra-jsonb-cache-key-duplicate-04/case_record.md's §5 scope note
-- previously stated as "standard, well-known PostgreSQL jsonb behavior, not
-- fabricated" but had not independently demonstrated against real Postgres.
--
-- Run: docker exec <container> psql -U postgres -d <db> -f this file
-- (or paste each statement into psql directly, as was done to produce the
-- output recorded in the case record).

CREATE TABLE jsonb_test (id serial, data jsonb);
CREATE TABLE text_test (id serial, data text);

INSERT INTO jsonb_test (data) VALUES
  ('{"reasoningId": "rs_abc123", "summary": "thinking...", "encrypted": false}');
INSERT INTO text_test (data) VALUES
  ('{"reasoningId": "rs_abc123", "summary": "thinking...", "encrypted": false}');

-- Observed result (real run, 2026-09-11, postgres:16 Docker image):
--   jsonb_test.data::text -> {"summary": "thinking...", "encrypted": false, "reasoningId": "rs_abc123"}
--   text_test.data        -> {"reasoningId": "rs_abc123", "summary": "thinking...", "encrypted": false}
-- The jsonb column genuinely reordered the keys; the text column preserved
-- insertion order exactly. This is real, observed PostgreSQL behavior, not
-- an assumption.
SELECT data::text FROM jsonb_test;
SELECT data FROM text_test;
