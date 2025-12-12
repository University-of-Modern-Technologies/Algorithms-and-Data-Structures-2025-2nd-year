from time import sleep
import heapq


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, task, priority):
        heapq.heappush(self.queue, (priority, task))

    def dequeue(self):
        return heapq.heappop(self.queue)[1]

    def is_empty(self):
        return not bool(self.queue)


def convert_doc_to_pdf(doc_path, pdf_path):
    print(f"Converting {doc_path} to {pdf_path} ...")
    sleep(0.5)
    return f"{pdf_path}.pdf"
