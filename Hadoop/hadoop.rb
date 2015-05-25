name "hadoop"
description "set Hadoop attributes"
default_attributes(
  "hadoop" => {
    "distribution" => "bigtop",
    "core_site" => {
      "fs.defaultFS" => "hdfs://hadoop1"
    },
    "yarn_site" => {
      "yarn.resourcemanager.hostname" =>"wikimedia-project"
    }
  }
)
run_list(
  "recipe[hadoop]"
)
