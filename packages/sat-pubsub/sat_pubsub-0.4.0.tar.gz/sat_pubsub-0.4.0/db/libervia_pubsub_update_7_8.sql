-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='7' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 7, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* new "overwrite_policy" option */
ALTER TABLE nodes ADD COLUMN overwrite_policy text NOT NULL DEFAULT 'original_publisher'
	CHECK (overwrite_policy IN ('original_publisher', 'any_publisher'));

UPDATE metadata SET value='8' WHERE key='version';
