from concurrent import futures
import grpc
import time
import chat_pb2_grpc as rpc
import chat_pb2 as chat__pb2
import redis


class ChatServer(rpc.ChatServiceServicer):
    def __init__(self):
        self.TTL = 10
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def ChatStream(self, request_iterator, context):
        last_index = 0
        while True:
            keys_list = f"messages"
            chat_length = self.redis_client.llen(keys_list)
            while chat_length > last_index:
                message_key = self.redis_client.lindex(keys_list, last_index)
                print(f'MESSAGE KEY: {message_key}')
                message_data = self.redis_client.get(message_key.decode('utf-8'))
                print(f'MESSAGE BEFORE: {message_data}')
                if message_data:
                    message_data = message_data.decode('utf-8')
                    print(f'MESSAGE : {message_data}')
                    sender, message = message_data.split(':', 1)
                    mess = chat__pb2.Message(username=sender, message=message)
                    yield mess
                last_index += 1

    def SendMessage(self, request, context):
        print(f"[{request.username}] {request.message}")
        message_key = f"msg:messages:{self.redis_client.incr('msg_id')}"
        message_data = f"{request.username}:{request.message}"

        self.redis_client.setex(message_key, self.TTL, message_data)
        # Store message in Redis cache
        self.redis_client.rpush('messages', message_key)
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