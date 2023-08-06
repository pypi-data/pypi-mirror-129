-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='8' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 8, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* new "roster" table */
CREATE TABLE roster (
     roster_id serial PRIMARY KEY,
     jid text NOT NULL UNIQUE,
     version text,
     updated timestamp with time zone NOT NULL,
     roster xml NOT NULL
);

UPDATE metadata SET value='9' WHERE key='version';
