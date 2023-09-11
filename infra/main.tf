module "mongodb_atlas" {
    source        = "./modules"
    mongodb_atlas_public_key = var.mongodb_atlas_public_key
    mongodb_atlas_private_key = var.mongodb_atlas_private_key
    org_id = var.org_id
    mongodb_atlas_database_username = var.mongodb_atlas_database_username
    mongodb_atlas_database_user_password = var.mongodb_atlas_database_user_password
}