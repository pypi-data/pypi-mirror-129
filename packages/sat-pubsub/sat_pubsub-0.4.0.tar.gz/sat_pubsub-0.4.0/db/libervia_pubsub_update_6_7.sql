-- NOTE: this update is to be used only by people which have been installing the
-- 6th version of the schema. It is has been replaced because regconfig prevent
-- proper update (the GENERATED column with regconfig has been replaced by a
-- trigger). People which haven't installed 6th version can directly use the
-- sat_pubsub_update_5_7.sql file. The sat_pubsub_update_5_6.sql has been
-- deleted has it's not needed anymore and can lead to troubles.

-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='6' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 6, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* regconfig type is not usable when doing database upgrade (for new PostgreSQL major version) */
ALTER TABLE items DROP COLUMN data_fts;
ALTER TABLE items ALTER COLUMN data_fts_cfg TYPE text;
ALTER TABLE items ADD COLUMN data_fts tsvector;
CREATE INDEX items_data_fts ON items USING GIN (data_fts);

ALTER FUNCTION update_data_fts() RENAME TO update_data_fts_cfg;
/* We don't use regconfig anymore in this method */
CREATE OR REPLACE FUNCTION update_data_fts_cfg() RETURNS TRIGGER AS
$$
BEGIN
    UPDATE items SET data_fts_cfg=replace(new.fts_language, 'generic', 'simple')
        WHERE items.node_id=new.node_id
            AND NOT EXISTS(SELECT FROM item_languages AS lang WHERE lang.item_id=items.item_id);
    RETURN new;
END;
$$
language plpgsql;

CREATE FUNCTION update_data_fts() RETURNS TRIGGER AS
$$
BEGIN
  new.data_fts=to_tsvector(new.data_fts_cfg::regconfig, new.data::text);
  RETURN new;
END
$$
language plpgsql;

CREATE TRIGGER items_fts_tsvector_update
     BEFORE INSERT OR UPDATE OF data_fts_cfg,data ON items
     FOR EACH ROW
     EXECUTE PROCEDURE update_data_fts();

/* We do the update to trigger the data_fts generation */
UPDATE items SET data_fts_cfg='simple';

UPDATE metadata SET value='7' WHERE key='version';
