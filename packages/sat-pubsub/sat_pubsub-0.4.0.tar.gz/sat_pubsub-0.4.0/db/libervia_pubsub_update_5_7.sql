-- we check version of the database before doing anything
-- and stop execution if not good
\set ON_ERROR_STOP
DO $$
DECLARE ver text;
BEGIN
    SELECT value INTO ver FROM metadata WHERE key='version';
    IF NOT FOUND OR ver!='5' THEN
        RAISE EXCEPTION 'This update file needs to be applied on database schema version 5, you use version %',ver;
    END IF;
END$$;
\unset ON_ERROR_STOP
-- end of version check

/* NOT NULL constraint was not applied to items.data */
ALTER TABLE items ALTER COLUMN data SET NOT NULL;

/* Full Text Search */
ALTER TABLE nodes ADD COLUMN fts_language text NOT NULL DEFAULT 'generic';
ALTER TABLE items ADD COLUMN data_fts_cfg text NOT NULL DEFAULT 'simple';
ALTER TABLE items ADD COLUMN data_fts tsvector;
CREATE INDEX items_data_fts ON items USING GIN (data_fts);

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

CREATE TRIGGER nodes_fts_language_update
     AFTER UPDATE OF fts_language ON nodes
     FOR EACH ROW
     EXECUTE PROCEDURE update_data_fts_cfg();

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

/* we update nodes with schema to prepare for XEP-0346 implementation */

INSERT INTO nodes(node, pep, persist_items, publish_model, max_items)
    SELECT 'fdp/template/'||s.node, s.pep, true, s.publish_model, 1
    FROM (
        SELECT node_id, node, pep, publish_model, schema
        FROM nodes
        WHERE schema IS NOT NULL
    ) AS s;

INSERT INTO affiliations(entity_id, node_id, affiliation)
    SELECT aff.entity_id, tpl.node_id, 'owner'
    FROM (
        SELECT node_id, node, pep, publish_model, schema
        FROM nodes
        WHERE schema IS NOT NULL AND pep IS NOT NULL
    ) AS s
    LEFT JOIN nodes AS tpl ON tpl.node='fdp/template/'||s.node AND tpl.pep=s.pep
    LEFT JOIN affiliations AS aff ON aff.node_id=s.node_id AND aff.affiliation='owner';

/* we need to do a similar request for non PEP nodes */
INSERT INTO affiliations(entity_id, node_id, affiliation)
    SELECT aff.entity_id, tpl.node_id, 'owner'
    FROM (
        SELECT node_id, node, pep, publish_model, schema
        FROM nodes
        WHERE schema IS NOT NULL AND pep IS NULL
    ) AS s
    LEFT JOIN nodes AS tpl ON tpl.node='fdp/template/'||s.node AND tpl.pep IS NULL
    LEFT JOIN affiliations AS aff ON aff.node_id=s.node_id AND aff.affiliation='owner';

INSERT INTO items(node_id, item, publisher, data)
    SELECT
        tpl.node_id,
        'current',
        e.jid||'/generated',
        xmlelement(name item, xmlattributes('current' as id, e.jid||'/generated' as publisher), s.schema)
    FROM (
        SELECT node_id, node, pep, publish_model, schema
        FROM nodes
        WHERE schema IS NOT NULL AND pep IS NOT NULL
    ) AS s
    LEFT JOIN nodes AS tpl ON tpl.node='fdp/template/'||s.node AND tpl.pep=s.pep
    LEFT JOIN affiliations AS aff ON aff.node_id = tpl.node_id AND aff.affiliation='owner'
    LEFT JOIN entities AS e ON e.entity_id = aff.entity_id;

/* once again for non PEP nodes */
INSERT INTO items(node_id, item, publisher, data)
    SELECT
        tpl.node_id,
        'current',
        e.jid||'/generated',
        xmlelement(name item, xmlattributes('current' as id, e.jid||'/generated' as publisher), s.schema)
    FROM (
        SELECT node_id, node, pep, publish_model, schema
        FROM nodes
        WHERE schema IS NOT NULL AND pep IS NULL
    ) AS s
    LEFT JOIN nodes AS tpl ON tpl.node='fdp/template/'||s.node AND tpl.pep IS NULL
    LEFT JOIN affiliations AS aff ON aff.node_id = tpl.node_id AND aff.affiliation='owner'
    LEFT JOIN entities AS e ON e.entity_id = aff.entity_id;

UPDATE nodes SET node='fdp/submitted/'||node WHERE schema IS NOT NULL;

UPDATE metadata SET value='7' WHERE key='version';
