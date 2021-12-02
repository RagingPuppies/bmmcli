# bmmcli Docs
This CLI let you control your brooklin cluster without messing with APIs and JSON string.
## Install
### Mac
To install it on a mac run the bellow command:
```
curl -sSL "" | sh
```
Once finish you can access your home directory and edit `bmm_config`
## Usage
```
# List all streams in a cluster
bmmcli list --cluster

# Get stream information, Status, Destination, Source and Topics
bmmcli describe --cluster <cluster_name> --stream <stream1>,<stream2>

# Delete a stream or streams
bmmcli delete <cluster_name> --stream <stream1>,<stream2>

# Pause a stream or streams
bmmcli pause --cluster <cluster_name> --stream <stream1> 

# resume a stream or streams
bmmcli resume --cluster <cluster_name> --stream <stream1> 

# Restarts a stream or streams ( pause and resume after 60s)
bmmcli restart --cluster <cluster_name> --stream <stream1> 

# Add Topics to a stream
bmmcli add-topic --cluster <cluster_name> --stream <stream1>,<stream2> --topic topic1,topic2

# Remove Topics to a stream
bmmcli remove-topic --cluster <cluster_name> --stream <stream1>,<stream2> -topic topic1,topic2
```

