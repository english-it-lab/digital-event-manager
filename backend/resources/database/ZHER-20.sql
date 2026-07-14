ALTER TABLE people
ADD COLUMN is_deleted boolean DEFAULT FALSE;

ALTER TABLE participants
ADD COLUMN is_deleted boolean DEFAULT FALSE;

ALTER TABLE sections
ADD COLUMN is_deleted boolean DEFAULT FALSE;
