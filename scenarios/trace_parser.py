from datetime import datetime
import re
import json


class MassaTraceParser:
    def __init__(self, feed_fn):
        self.feed_fn = feed_fn
        self.offset = 0

    def get_trace_logs(self):
        log_lines = self.feed_fn(self.offset)
        self.offset += len(log_lines)
        result = []
        for log_line in log_lines:
            parsed_line = self._parse_trace_log(log_line)
            if parsed_line is not None:
                result.append(parsed_line)
        return result

    @staticmethod
    def _parse_trace_log(log_line):
        #Remove color string
        log_line = re.sub(r'\x1b\[\d+m', '', log_line)
        match_result = re.match(
            r"(?P<date>(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})? TRACE massa_network::network_worker: massa:peer_list_received:(?P<message>.*)$", log_line)
        if match_result is None:
            return None
        # noinspection PyBroadException
        try:
            message = json.loads(match_result.group("message"))
            message["date"] = datetime.fromisoformat(match_result.group("date"))
        except Exception as e:
            return None
        return message
