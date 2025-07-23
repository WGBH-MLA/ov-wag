-- SQL Migration Script: Convert Collection to inherit from CollectionPage
-- This script migrates existing Collection records to use the new inheritance structure
-- where Collection inherits from CollectionPage instead of Page directly.

-- IMPORTANT: Backup your database before running this script!

BEGIN;

-- Step 1: Create CollectionPage records for each existing Collection
-- This will create the "parent" records that Collection will inherit from
INSERT INTO ov_collections_collectionpage (
    page_ptr_id,
    introduction,
    cover_image_id,
    hero_image_id,
    featured
)
SELECT 
    c.page_ptr_id,
    c.introduction,
    c.cover_image_id,
    c.hero_image_id,
    c.featured
FROM ov_collections_collection c
WHERE c.page_ptr_id NOT IN (
    SELECT page_ptr_id FROM ov_collections_collectionpage
);

-- Step 2: Update the content_type for pages that are now CollectionPages
-- ContentType ID 74 is for CollectionPage, ID 32 is for Collection
UPDATE wagtailcore_page 
SET content_type_id = 74 
WHERE id IN (
    SELECT page_ptr_id FROM ov_collections_collectionpage
);

-- Step 3: Add collectionpage_ptr_id to Collection table temporarily as nullable
-- (This should already exist from the migration, but ensuring it's there)
-- ALTER TABLE ov_collections_collection ADD COLUMN IF NOT EXISTS collectionpage_ptr_id INTEGER;

-- Step 4: Update Collection records to point to their corresponding CollectionPage
UPDATE ov_collections_collection 
SET collectionpage_ptr_id = page_ptr_id
WHERE collectionpage_ptr_id IS NULL;

-- Step 5: Verify the data migration
-- This query should return the count of collections that have been migrated
SELECT 
    'Collections migrated:' as status,
    COUNT(*) as count
FROM ov_collections_collection c
JOIN ov_collections_collectionpage cp ON c.collectionpage_ptr_id = cp.page_ptr_id;

-- Step 6: Check for any orphaned records
SELECT 
    'Collections without CollectionPage:' as status,
    COUNT(*) as count
FROM ov_collections_collection c
LEFT JOIN ov_collections_collectionpage cp ON c.page_ptr_id = cp.page_ptr_id
WHERE cp.page_ptr_id IS NULL;

-- If you're satisfied with the migration, you can run the final steps:
-- These would normally be done in a Django migration, but we'll prepare them here

/*
-- Step 7: Remove duplicate fields from Collection table
-- (Uncomment these when ready to finalize the migration)

-- ALTER TABLE ov_collections_collection DROP COLUMN introduction;
-- ALTER TABLE ov_collections_collection DROP COLUMN cover_image_id;
-- ALTER TABLE ov_collections_collection DROP COLUMN hero_image_id;
-- ALTER TABLE ov_collections_collection DROP COLUMN featured;
-- ALTER TABLE ov_collections_collection DROP COLUMN page_ptr_id;

-- Step 8: Make collectionpage_ptr_id the primary key and non-nullable
-- ALTER TABLE ov_collections_collection ALTER COLUMN collectionpage_ptr_id SET NOT NULL;
-- ALTER TABLE ov_collections_collection DROP CONSTRAINT ov_collections_collection_pkey;
-- ALTER TABLE ov_collections_collection ADD PRIMARY KEY (collectionpage_ptr_id);
*/

COMMIT;

-- Verification queries to run after the migration:
SELECT 
    'Final verification - Collections:' as table_name,
    COUNT(*) as count
FROM ov_collections_collection;

SELECT 
    'Final verification - CollectionPages:' as table_name,
    COUNT(*) as count
FROM ov_collections_collectionpage;

-- Check that all collections have corresponding collection pages
SELECT 
    c.page_ptr_id as collection_page_id,
    cp.page_ptr_id as collectionpage_page_id,
    p.title,
    c.collectionpage_ptr_id
FROM ov_collections_collection c
JOIN ov_collections_collectionpage cp ON c.collectionpage_ptr_id = cp.page_ptr_id
JOIN wagtailcore_page p ON cp.page_ptr_id = p.id
LIMIT 5;
