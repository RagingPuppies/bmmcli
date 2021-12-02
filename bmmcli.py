import argparse, configparser, time, os.path
from stream import bmmcli 
from extras import csv_to_list, validateCluster, pretty ,switch, case

__author__ = "Tomer Setty AKA RagingPuppies"

config_file_path = (os.path.expanduser('~') + '/bmm_config')
config = configparser.ConfigParser()
config.read(config_file_path)

if not os.path.isfile(config_file_path):
    print("Please place ~/bmm_config in your home folder.")
    exit(1)

parser = argparse.ArgumentParser(description='Brooklin command line interface. V1.0')

subparser = parser.add_subparsers(dest='command')

list = subparser.add_parser('list')
list.add_argument('--cluster', type=str, required=True,
                    help='Enter a cluster name from the bmm_config file, All datastreams from this cluster will be printed.')

describe = subparser.add_parser('describe')
describe.add_argument('--cluster', type=str, required=True)
describe.add_argument('--stream', type=str, required=True,
                        help='One or more streams, Seperated by a comma, Will show a readable stream information and a list of active topics.')

delete = subparser.add_parser('delete')
delete.add_argument('--cluster', type=str, required=True)
delete.add_argument('--stream', type=str, required=True,
                        help='One or more streams te delete, Seperated by a comma, will delete each stream listed here.')

add_topic = subparser.add_parser('add-topic')
add_topic.add_argument('--cluster', type=str, required=True)
add_topic.add_argument('--stream', type=str, required=True,
                        help='One or more streams, Seperated by a comma.')
add_topic.add_argument('--topic', type=str, required=True,
                        help='One or more topics to add, Seperated by a comma.')

remove_topic = subparser.add_parser('remove-topic')
remove_topic.add_argument('--cluster', type=str, required=True)
remove_topic.add_argument('--stream', type=str, required=True,
                        help='One or more streams, Seperated by a comma.')
remove_topic.add_argument('--topic', type=str, required=True,
                        help='One or more topics to delete, Seperated by a comma.')

restart = subparser.add_parser('restart')
restart.add_argument('--cluster', type=str, required=True)
restart.add_argument('--stream', type=str, required=True,
                        help='One or more streams, Seperated by a comma.')

pause = subparser.add_parser('pause')
pause.add_argument('--cluster', type=str, required=True)
pause.add_argument('--stream', type=str, required=True,
                        help='One or more streams, Seperated by a comma.')

resume = subparser.add_parser('resume')
resume.add_argument('--cluster', type=str, required=True)
resume.add_argument('--stream', type=str, required=True,
                        help='One or more streams, Seperated by a comma.')

args = parser.parse_args()

cluster = args.cluster

validateCluster(cluster, config)

bmm_client = bmmcli(config[cluster]['url'], config[cluster]['port'])

while switch(args.command):
    if case('list'):
        bmm_client.list_streams()
        break

    if case('describe'):
        streams = csv_to_list(args.stream)
        for stream in streams:
            pretty(bmm_client.get_stream(stream))
        break

    if case('create'):
        print("Method not supported.")
        break

    if case('delete'):
        if input("are you sure you want to delete: " + args.stream + " ? (y/n)") != "y":
            exit(0)
        streams = csv_to_list(args.stream)
        if bmm_client.get_stream(streams).status_code == 404:
            print("Streams does not exist, nothing to delete.")
            break
        else:
            bmm_client.delete_stream(streams)
            break

    if case('add-topic'):
        streams = csv_to_list(args.stream)
        topics = csv_to_list(args.topic)
        bmm_client.add_topics(topics, streams)
        break

    if case('remove-topic'):
        streams = csv_to_list(args.stream)
        topics = csv_to_list(args.topic)
        bmm_client.remove_topics(topics, streams)
        break

    if case('pause'):
        streams = csv_to_list(args.stream)
        bmm_client.toggle_stream(streams, "pause")
        break

    if case('resume'):
        streams = csv_to_list(args.stream)
        bmm_client.toggle_stream(streams, "resume")
        break

    if case('restart'):
        streams = csv_to_list(args.stream)
        print("Pause and resume a stream, will take a minute... please wait.")
        bmm_client.toggle_stream(streams, "pause")
        time.sleep(60)
        bmm_client.toggle_stream(streams, "resume")
        break

    raise Exception("no valid method entered.")
    break
