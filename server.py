from concurrent import futures

import grpc
import time

import chat_pb2_grpc as rpc
import chat_pb2 as chat__pb2


class ChatServer(rpc.ChatServiceServicer):
    def __init__(self):
        self.message_history = []

    def ChatStream(self, request_iterator, context):
        last_index = 0
        while True:
            while len(self.message_history) > last_index:
                next_message = self.message_history[last_index]
                last_index += 1
                yield next_message

    def SendMessage(self, request, context):
        print(f"[{request.username}] {request.message}")
        self.message_history.append(request)
        return chat__pb2.Empty()


if __name__ == '__main__':
    port = 8080
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_ChatServiceServicer_to_server(ChatServer(), server)
    print('Initializing server. Now listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    while True:
        time.sleep(1e6)
