CREATE TABLE entities (
    entity_id serial PRIMARY KEY,
    jid text NOT NULL UNIQUE
);

CREATE TABLE nodes (
    node_id serial PRIMARY KEY,
    node text NOT NULL,
    pep text,
    node_type text NOT NULL DEFAULT 'leaf'
        CHECK (node_type IN ('leaf', 'collection')),
    access_model text NOT NULL DEFAULT 'open'
        CHECK (access_model IN ('open', 'presence', 'publisher-roster', 'whitelist', 'publish-only', 'self-publisher')),
    persist_items boolean,
    deliver_payloads boolean NOT NULL DEFAULT TRUE,
    max_items integer NOT NULL DEFAULT 0
        CHECK (max_items >= 0),
	overwrite_policy text NOT NULL DEFAULT 'original_publisher'
		CHECK (overwrite_policy IN ('original_publisher', 'any_publisher')),
    serial_ids boolean NOT NULL DEFAULT FALSE,
    consistent_publisher boolean NOT NULL DEFAULT FALSE,
    fts_language text NOT NULL DEFAULT 'generic',
    send_last_published_item text NOT NULL DEFAULT 'on_sub'
        CHECK (send_last_published_item IN ('never', 'on_sub')),
    publish_model text NOT NULL DEFAULT 'publishers'
        CHECK (publish_model IN ('publishers', 'subscribers', 'open')),
    schema xml
);

/* we need 2 partial indexes to manage NULL value for PEP */
CREATE UNIQUE INDEX nodes_node_pep_key_not_null ON nodes(node, pep) WHERE pep IS NOT NULL;
CREATE UNIQUE INDEX nodes_node_pep_key_null ON nodes(node) WHERE pep IS NULL;

INSERT INTO nodes (node, node_type) values ('', 'collection');

CREATE TABLE affiliations (
    affiliation_id serial PRIMARY KEY,
    entity_id integer NOT NULL REFERENCES entities ON DELETE CASCADE,
    node_id integer NOT NULL references nodes ON DELETE CASCADE,
    affiliation text NOT NULL
        CHECK (affiliation IN ('outcast', 'member', 'publisher', 'owner')),
    UNIQUE (entity_id, node_id)
);

CREATE TABLE node_groups_authorized (
    node_groups_authorized_id serial PRIMARY KEY,
    node_id integer NOT NULL references nodes ON DELETE CASCADE,
    groupname text NOT NULL,
    UNIQUE (node_id,groupname)
);

CREATE TABLE subscriptions (
    subscription_id serial PRIMARY KEY,
    entity_id integer NOT NULL REFERENCES entities ON DELETE CASCADE,
    resource text,
    node_id integer NOT NULL REFERENCES nodes ON delete CASCADE,
    state text NOT NULL DEFAULT 'subscribed'
        CHECK (state IN ('subscribed', 'pending', 'unconfigured')),
    subscription_type text
        CHECK (subscription_type IN (NULL, 'items', 'nodes')),
    subscription_depth text
        CHECK (subscription_depth IN (NULL, '1', 'all')),
    UNIQUE (entity_id, resource, node_id));

CREATE TABLE items (
    item_id serial PRIMARY KEY,
    node_id integer NOT NULL REFERENCES nodes ON DELETE CASCADE,
    item text NOT NULL,
    publisher text NOT NULL,
    data xml NOT NULL,
    data_fts tsvector,
    data_fts_cfg text NOT NULL DEFAULT 'simple',
    access_model text NOT NULL DEFAULT 'open'
        CHECK (access_model IN ('open', 'publisher-roster', 'whitelist')),
    created timestamp with time zone NOT NULL DEFAULT now(),
    updated timestamp with time zone NOT NULL DEFAULT now(),
    UNIQUE (node_id, item)
);

CREATE TABLE item_groups_authorized (
    item_groups_authorized_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    groupname text NOT NULL,
    UNIQUE (item_id,groupname)
);

CREATE TABLE item_jids_authorized (
    item_jids_authorized_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    jid text NOT NULL,
    UNIQUE (item_id,jid)
);

CREATE TABLE item_languages (
    item_languages_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    language text NOT NULL,
    UNIQUE (item_id,language)
);

CREATE TABLE item_categories (
    item_categories_id serial PRIMARY KEY,
    item_id integer NOT NULL references items ON DELETE CASCADE,
    category text NOT NULL,
    UNIQUE (item_id,category)
);

/* Full Text Search */
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

/* Roster */

CREATE TABLE roster (
     roster_id serial PRIMARY KEY,
     jid text NOT NULL UNIQUE,
     version text,
     updated timestamp with time zone NOT NULL,
     roster xml NOT NULL
);


CREATE TABLE metadata (
    key text PRIMARY KEY,
    value text
);

INSERT INTO metadata VALUES ('version', '9');
