#!/bin/bash

# local machine mongodb dir configurations
readonly root_dir="$HOME/mongoDB"
readonly data_path="$root_dir/data"
readonly config_path="$root_dir/config"
readonly log_path="$root_dir/log"
readonly resource_path="$root_dir/resource"

# mongodb files names
readonly config_name="mongod.conf"
readonly log_name="mongod.log"
readonly db_file_name="db_init.js"  # initialize the database

# mongodb files paths
readonly config_file_path="$config_path/$config_name"
readonly log_file_path="$log_path/$log_name"

# intialize the directories
function init_dir() {
	if [ ! -d "$root_dir" ]; then
    mkdir "$root_dir" && mkdir "$data_path" && mkdir "$config_path" && mkdir "$log_path" && mkdir "$resource_path"
fi
}

# initialize the files
function init_file() {
	umask 0111

	# create files
	touch "$config_file_path"
	touch "$log_file_path"

	# configurations
	cat <<- EOF > "$config_file_path"
processManagement:
   fork: false
net:
   bindIp: 0.0.0.0
   port: 27018
storage:
   dbPath: /data/db
systemLog:
   destination: file
   path: /var/log/mongo/mongod.log
   logAppend: true
storage:
   journal:
      enabled: true
security:
      authorization: enabled
EOF

	cp "$(pwd)/init/resource/$db_file_name" "$resource_path"
	sudo chmod 755 "$resource_path/$db_file_name"
}

function create_container() {
	sudo docker run --name wb_spider --privileged --restart=always  \
  -p 27018:27018 \
  -v "$data_path":/data/db \
  -v "$log_path":/var/log/mongo \
  -v "$config_path":/etc/mongo \
  -v "$resource_path":/etc/resource \
  -d mongo:4.2 -f /etc/mongo/mongod.conf
}


function main() {
	if [ -d "$root_dir" ]; then
		sudo rm -r "$root_dir"
fi

	init_dir
	echo "Directories initialized"
	init_file
	echo "Files initialized"
	create_container
	echo "Container created"

	cat <<-EOF
Run command
	"sudo docker exec -it wb_spider mongo 127.0.0.1:27018 /etc/resource/db_init.js"
EOF
}


main