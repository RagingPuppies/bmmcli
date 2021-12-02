import requests



class bmmcli(object):
    def __init__(self, service, port=32311):
        self.url = self.construct_url(service, port)

    def construct_url(self, service, port):
        return service + ":" + port

    def list_streams(self):
        url = self.url + "/datastream/"
        data = requests.get(url).json()
        for stream in data["elements"]:
            print(stream["name"])

    def get_stream(self, stream):
        url = self.url + "/datastream/" + stream
        data = requests.get(url)
        return data

    def delete_stream(self, streams):
        for stream in streams:
            url = self.url + "/datastream/" + stream
            requests.delete(url)

    def toggle_stream(self, streams, action):
        for stream in streams:
            url = self.url + "/datastream/" + stream + "?action=" + action
            requests.post(url)

    def rewrite_metadata(self, metadata, topics):
        metadata_part_a = str(metadata).split("(")[0]
        metadata_part_b = str(metadata).split(")")[1]
        new_metadata = metadata_part_a + "(" + topics + ")" + metadata_part_b
        return new_metadata

    def compare_topics_to_add(self, new_topics, metadata):
        s = metadata["source"]["connectionString"]
        old_topics_list = (s[s.find("(")+1:s.find(")")]).split("|")
        resulting_list = list(old_topics_list)
        resulting_list.extend(x for x in new_topics if x not in resulting_list)
        topic_final = "|".join(resulting_list)
        return topic_final

    def compare_topics_to_remove(self, new_topics, metadata):
        s = metadata["source"]["connectionString"]
        old_topics_list = (s[s.find("(")+1:s.find(")")]).split("|")
        for topic in new_topics:
            if topic in old_topics_list:
                old_topics_list.remove(topic)
            else:
                print(topic, "does not exist in the datastream.")
        topic_final = "|".join(old_topics_list)
        return topic_final

    def update_stream(self, x, stream):  
        url = self.url + "/datastream/" + stream 
        data = x.replace("'", '"')
        requests.put(url, data=data, headers={'content-type':'application/json'})

    def add_topics(self, topics, streams):
        for stream in streams:
            metadata = self.get_stream(stream).json()
            topic_final = self.compare_topics_to_add(topics, metadata)
            new_metadata = self.rewrite_metadata(metadata, topic_final)
            self.update_stream(new_metadata, stream)

    def remove_topics(self, topics, streams):
        for stream in streams:
            metadata = self.get_stream(stream).json()
            topic_final = self.compare_topics_to_remove(topics, metadata)
            new_metadata = self.rewrite_metadata(metadata, topic_final)
            self.update_stream(new_metadata, stream)
            

