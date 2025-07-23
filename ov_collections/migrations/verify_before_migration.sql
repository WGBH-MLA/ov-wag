-- Pre-migration verification script
-- Run this to check the current state before applying the migration

-- Check current Collection records
SELECT 
    'Current Collections:' as table_name,
    COUNT(*) as count
FROM ov_collections_collection;

-- Check current CollectionPage records
SELECT 
    'Current CollectionPages:' as table_name,
    COUNT(*) as count
FROM ov_collections_collectionpage;

-- Check Collection data structure
SELECT 
    c.page_ptr_id,
    p.title,
    p.content_type_id,
    ct.model as content_type,
    c.introduction IS NOT NULL as has_introduction,
    c.cover_image_id IS NOT NULL as has_cover_image,
    c.hero_image_id IS NOT NULL as has_hero_image,
    c.featured
FROM ov_collections_collection c
JOIN wagtailcore_page p ON c.page_ptr_id = p.id
JOIN django_content_type ct ON p.content_type_id = ct.id
LIMIT 5;

-- Check for any existing CollectionPage records that might conflict
SELECT 
    'Potential conflicts - Collections with existing CollectionPages:' as status,
    COUNT(*) as count
FROM ov_collections_collection c
JOIN ov_collections_collectionpage cp ON c.page_ptr_id = cp.page_ptr_id;
