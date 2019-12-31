import alb_access_log_helper

entries = alb_access_log_helper.get_high_latency_log_entries(path="sample_data", threshold=0.2)
for entry in entries:
    print(entry)