-- Rollback Script: Undo Collection to CollectionPage inheritance migration
-- This script reverses the changes made by migrate_collection_to_inheritance.sql

-- IMPORTANT: This will only work if you haven't run the final ALTER TABLE commands
-- that remove the original fields from the Collection table.

BEGIN;

-- Step 1: Restore the original content_type for Collection pages
-- ContentType ID 32 is for Collection
UPDATE wagtailcore_page 
SET content_type_id = 32 
WHERE id IN (
    SELECT c.page_ptr_id 
    FROM ov_collections_collection c
    JOIN ov_collections_collectionpage cp ON c.collectionpage_ptr_id = cp.page_ptr_id
);

-- Step 2: If the original fields were removed, restore them from CollectionPage
-- (Only run these if the fields were dropped)
/*
-- Restore the fields if they were dropped
ALTER TABLE ov_collections_collection ADD COLUMN IF NOT EXISTS introduction text;
ALTER TABLE ov_collections_collection ADD COLUMN IF NOT EXISTS cover_image_id integer;
ALTER TABLE ov_collections_collection ADD COLUMN IF NOT EXISTS hero_image_id integer;
ALTER TABLE ov_collections_collection ADD COLUMN IF NOT EXISTS featured boolean;

-- Copy data back from CollectionPage
UPDATE ov_collections_collection 
SET 
    introduction = cp.introduction,
    cover_image_id = cp.cover_image_id,
    hero_image_id = cp.hero_image_id,
    featured = cp.featured
FROM ov_collections_collectionpage cp
WHERE ov_collections_collection.collectionpage_ptr_id = cp.page_ptr_id;
*/

-- Step 3: Clear the collectionpage_ptr_id references
UPDATE ov_collections_collection 
SET collectionpage_ptr_id = NULL;

-- Step 4: Delete the CollectionPage records (this will cascade and clean up)
DELETE FROM ov_collections_collectionpage 
WHERE page_ptr_id IN (
    SELECT page_ptr_id FROM ov_collections_collection
);

-- Verification
SELECT 
    'Collections after rollback:' as status,
    COUNT(*) as count
FROM ov_collections_collection;

SELECT 
    'CollectionPages after rollback:' as status,
    COUNT(*) as count
FROM ov_collections_collectionpage;

COMMIT;
