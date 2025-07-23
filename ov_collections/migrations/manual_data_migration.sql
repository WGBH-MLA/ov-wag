-- Manual data migration: Create CollectionPage records and link them to Collections
-- Run this before applying the final schema migration

BEGIN;

-- Get the ContentType ID for CollectionPage
-- You may need to adjust this ID based on your database
-- Run: SELECT id FROM django_content_type WHERE model = 'collectionpage';
-- Expected to be around 74, but verify first!

-- Step 1: Create CollectionPage records for each Collection
INSERT INTO ov_collections_collectionpage (
    page_ptr_id,
    introduction,
    cover_image_id,
    hero_image_id,
    featured
)
SELECT 
    c.page_ptr_id,
    COALESCE(c.introduction, ''),
    c.cover_image_id,
    c.hero_image_id,
    COALESCE(c.featured, false)
FROM ov_collections_collection c
WHERE c.page_ptr_id NOT IN (
    SELECT page_ptr_id FROM ov_collections_collectionpage
);

-- Step 2: Update page content_type to CollectionPage (ID 74 - verify this!)
UPDATE wagtailcore_page 
SET content_type_id = (
    SELECT id FROM django_content_type WHERE model = 'collectionpage' AND app_label = 'ov_collections'
)
WHERE id IN (
    SELECT page_ptr_id FROM ov_collections_collectionpage
);

-- Step 3: Fix any null values in pages that might cause issues
UPDATE wagtailcore_page 
SET 
    title = COALESCE(title, 'Collection ' || id::text),
    slug = COALESCE(slug, 'collection-' || id::text),
    path = COALESCE(path, LPAD(id::text, 4, '0')),
    depth = COALESCE(depth, 2),
    numchild = COALESCE(numchild, 0)
WHERE id IN (
    SELECT page_ptr_id FROM ov_collections_collectionpage
);

-- Verification
SELECT 
    'Collections:' as table_name,
    COUNT(*) as count
FROM ov_collections_collection;

SELECT 
    'CollectionPages:' as table_name,
    COUNT(*) as count
FROM ov_collections_collectionpage;

-- Check that all collections have corresponding collection pages
SELECT 
    'Collections with matching CollectionPages:' as status,
    COUNT(*) as count
FROM ov_collections_collection c
JOIN ov_collections_collectionpage cp ON c.page_ptr_id = cp.page_ptr_id;

COMMIT;
