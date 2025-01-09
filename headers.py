import header_proc_state as proc_state
import table as tbl
import http2 as h2
import os


class header_frame:

    header_idx_position = 0

    def __init__(self):

        # self.frame = [raw_data[i:i + 2] for i in range(0, len(raw_data), 2)]
        self.frame = []
        # s = self.frame[:h2.http_frame.frame_payload_size_idx + 1]
        # self.payload_size = int('0x' + s[0] + s[1] + s[2], 0)
        # self.payload = self.frame[h2.http_frame.frame_header_size:]
        self.rst = []
        self.H = False
        self.expect_grpc_data = False
        self.head_name = ''
        self.head_val = ''
        self.idx = ''
        self.data_len = 0
        self.current_state = proc_state.state.IDEL
        self.tbl = tbl.table()
        self.frame = ''

    def __clear__(self):

        self.H = False
        self.head_name = ''
        self.head_val = ''
        self.idx = ''
        self.data_len = 0

    def process(self, raw_data):
        #self.frame = [raw_data[i:i + 2] for i in range(0, len(raw_data), 2)]
        self.frame = raw_data
        #breakpoint()
        s = self.frame[:h2.http_frame.frame_payload_size_idx + 1]
        self.payload_size = int('0x' + s[0] + s[1] + s[2], 0)
        self.payload = self.frame[h2.http_frame.frame_header_size:]
        self.current_state = proc_state.state.DETERMINE_TYPE
        #breakpoint()

        while (self.current_state != proc_state.state.IDEL):

            match self.current_state:
                case proc_state.state.DETERMINE_TYPE:
                    head_b = bin(int(self.payload[header_frame.header_idx_position], 16))[
                                 2:].zfill(8)
                    if (head_b[0] == '1'):
                        self.current_state = proc_state.state.DIRECT_GET
                        self.idx = str(int(head_b[1:], 2))
                    elif (head_b[1] == '1'):
                        self.current_state = proc_state.state.INSERT_TBL_NEED_NAME_VAL
                        self.idx = str(int(head_b[2:], 2))
                    else:
                        print(head_b)
                    self.payload = self.payload[1:]

                case proc_state.state.DIRECT_GET:

                    self.head_name = self.tbl.get_val(self.idx)
                    # here head_name has contained complete val, so I just set the head_val as a space char,
                    # to differentiated with null
                    self.head_val = ' '  # this is space char, NOT null
                    self.current_state = proc_state.state.CLEAN

                case proc_state.state.INSERT_TBL_NEED_NAME_VAL:
                    if self.idx != '0':  # lack both name and val
                        self.head_name = self.tbl.get_val(self.idx)

                    self.current_state = proc_state.state.GET_LEN

                case proc_state.state.GET_LEN:
                    len_b = bin(int(self.payload[header_frame.header_idx_position], 16))[
                                2:].zfill(8)
                    if len_b[0] == '1':
                        self.H = True
                    self.data_len = str(int(len_b[1:], 2))
                    self.payload = self.payload[1:]
                    self.current_state = proc_state.state.GET_DATA

                case proc_state.state.GET_DATA:
                    data = ''.join(self.payload[:int(self.data_len)])
                    
                    if self.H:
                        # breakpoint()
                        if data != '':
                            cmd = f'python3 hfm_decoder.py {data}'
                            val = os.popen(cmd).read().replace(
                                '\n', ' ').replace('\r', '')
                        else:
                            val = ' ' # a space char
                    else:
                        #print(data)
                        val = ''.join([chr(int(b, 16)) for b in [data[i:i+2] for i in range(0, len(data), 2)]])

                    if self.head_name == '':
                        self.head_name = val
                        self.current_state = proc_state.state.GET_LEN
                    else:
                        # breakpoint()
                        self.head_val = val
                        #print(val)
                        #if 'application/grpc' in val:
                            #self.expect_grpc_data = True
                        self.current_state = proc_state.state.CLEAN
                        self.tbl.insert_entry(
                            self.head_name + ' ' + self.head_val)

                    self.payload = self.payload[int(self.data_len):]

                case proc_state.state.CLEAN:
                    item = self.head_name + ' ' + self.head_val
                    item = item.rstrip()
                    self.rst.append(item)
                    if 'application/grpc' in item:
                            self.expect_grpc_data = True
                    #if len(self.rst) == 600:
                       #print(self.rst)
                       #breakpoint()
                    self.__clear__()
                    if len(self.payload) > 0:
                        self.current_state = proc_state.state.DETERMINE_TYPE
                    else:
                        self.current_state = proc_state.state.IDEL

        print(self.rst)
        self.rst = []
