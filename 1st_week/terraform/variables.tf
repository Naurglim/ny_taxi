variable "credentials" {
  description = "My Credentials"
  default     = "~/.gc/ny-rides.json"
}

variable "project" {
  description = "Project"
  default     = "ny-rides-gperezcenteno-411315"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default = "southamerica-west1-a"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "SOUTHAMERICA-WEST1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default = "ny_rides_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "ny-rides-gperezcenteno-411315-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}