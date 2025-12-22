from agents import Agent,Runner,set_trace_processors
from agents.tracing.processor_interface import TracingProcessor
from dotenv import load_dotenv
import os
from config import config
from pprint import pprint


load_dotenv()


class LocalTraceprocessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans =[]

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"the trace started{trace.trace_id}")

    def on_trace_end(self, trace):
        pprint(f"on trace ended {trace.export()}")


    def on_span_start(self, span):
        self.spans.append(span)
        print("on span start:")
        print("span details")
        pprint(span.export())

    def on_span_end(self, span):
        print("on span end:")
        print("span details")
        pprint(span.export())

    def force_flush(self):
        print("forcing flush data")

    def shutdown(self):
        print("shuting down","*" * 29)
        print("collected traces")
        for trace in self.traces:
            pprint(trace.export())
        print("collected span")
        for span in self.spans:
            pprint(span.export())


local_prcessor = LocalTraceprocessor()
set_trace_processors([local_prcessor])
agent = Agent(
    name="simple_agent",
    instructions="you are simple general assistant"
)

result =Runner.run_sync(agent,"what is the capital of pakistan")
print(result.final_output)