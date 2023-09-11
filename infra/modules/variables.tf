variable "project_name" {
    default =  "Task Board"
    description = "The name of the MongoDB Atlas project."
}

variable "cluster_name" {
    default =  "task-board-cluster"
    description = "The name of the MongoDB Atlas cluster."
}

variable "instance_size" {
    default = "M2"
    description = "The size of the MongoDB Atlas instance."
}

variable "mongodb_atlas_public_key" {
    description = "The MongoDB Atlas public key."
}

variable "mongodb_atlas_private_key" {
    description = "The MongoDB Atlas private key."
}

variable "org_id" {
    description = "The MongoDB Atlas organization ID."
}

variable "mongodb_atlas_database_username" {
    description = "The MongoDB Atlas database username."
}

variable "mongodb_atlas_database_user_password" {
    description = "The MongoDB Atlas database user password."
}