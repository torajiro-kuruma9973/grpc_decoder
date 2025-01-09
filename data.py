import http2 as ht2
import grpc as grpc
import os

class data_frame:

    def __init__(self):
        # http payload
        self.frame = ''
        self.http_payload_size = 0
        self.http_payload = []
        self.rst = {}
        #self.proto = proto_path

    def process(self, raw_data, flag):
        #print("######################")
        #print(raw_data)
        self.frame = raw_data
        self.http_payload_size = int('0x' + self.frame[0] + self.frame[1] + self.frame[2], 0)
        self.http_payload = self.frame[ht2.http_frame.frame_header_size:]
        if flag == True:
            s = self.http_payload
            self.grpc_payload_size = int('0x' + s[0] + s[1] + s[2] + s[3] + s[4], 0)
            self.grpc_payload = self.http_payload[grpc.grpc_frame.frame_header_size:]
            data_s = ''.join(self.grpc_payload)
            cmd = f'echo {data_s} | xxd -r -p | protoc --decode_raw'
            #print(cmd)
            val = os.popen(cmd).read()
            print(val)
            val = val.splitlines()
            
            for s in val:
                s = s.split()
                #print(s)
                k = s[0].rstrip().replace(':', '')
                if len(s) > 1:
                    self.rst[k] = s[1]
            #self.grpc = False
            #print(self.rst)
        else:
            print("No grpc data!")

    def print_rst(self):
        #print(self.rst)
        self.rst = {}