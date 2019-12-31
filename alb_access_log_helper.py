import os


def read_files(path="sample_data"):
    logs = []
    for file in os.listdir(path):
        f = open(os.path.join(path, file), "r")
        for line in f:
            logs.append(line)
    return logs


class AlbAccessLogEntry:
    """
    https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html#access-log-file-format
    """
    def __init__(self, entry):
        parsed_entry = entry.split(" ")
        self.type = parsed_entry[0]
        self.timestamp = parsed_entry[1]
        self.elb = parsed_entry[2]
        self.client_port = parsed_entry[3]
        self.target_port = parsed_entry[4]
        self.request_processing_time = float(parsed_entry[5])
        self.target_processing_time = float(parsed_entry[6])
        self.response_processing_time = float(parsed_entry[7])
        self.elb_status_code = parsed_entry[8]
        self.target_status_code = parsed_entry[9]
        self.received_bytes = parsed_entry[10]
        self.sent_bytes = parsed_entry[11]
        self.request = parsed_entry[12] + " " + parsed_entry[13] + " " + parsed_entry[14]
        self.user_agent = parsed_entry[15]
        self.ssl_cipher = parsed_entry[16]
        self.ssl_protocol = parsed_entry[17]
        self.target_group_arn = parsed_entry[18]
        self.trace_id = parsed_entry[19]
        self.domain_name = parsed_entry[20]
        self.chosen_cert_arn = parsed_entry[21]
        self.matched_rule_priority = parsed_entry[22]
        self.request_creation_time = parsed_entry[23]
        self.actions_executed = parsed_entry[24]
        self.redirect_url = parsed_entry[25]
        self.error_reason = parsed_entry[26]
        self.target_port_list = parsed_entry[27]
        self.target_status_code_list = parsed_entry[28]


def get_high_latency_log_entries(path="sample_data", threshold=0.0):
    entry_list = []
    log_entries = read_files(path)
    for entry in log_entries:
        entry_object = AlbAccessLogEntry(entry)
        if entry_object.target_processing_time > threshold:
            entry_list.append(entry)
    return entry_list

