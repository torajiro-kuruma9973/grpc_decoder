import headers as hds
import data as dt
import table as tbl
class http_frame:
    frame_header_size = 9
    frame_payload_size_idx = 2
    HTTP_DATA = 0
    HTTP_HEADERS = 1
    SETTINGS = 4

    def __init__(self):
        #self.data_list = []
        #print(self.data_list)
        self.c_hds = hds.header_frame()
        self.s_hds = hds.header_frame()
        self.hds = None
        self.dt = dt.data_frame()
    def process(self, s, flag):
        #s = self.data_list
        s = [s[i:i + 2] for i in range(0, len(s), 2)]
        #print(s)
        #breakpoint()

        if flag == 'c':
            self.hds = self.c_hds
        else:
            self.hds = self.s_hds
        while(len(s) > 0):
            size = int('0x' + s[0] + s[1] + s[2], 0)
            # 1. obtain the first frame type
            frame_type = int(s[3])
            sid_data = s[5:9]
            sid_data[0] = '0'
            stram_id = ''.join(sid_data)
            #stram_id = int('0x' + sid_data, 0)
            id = int('0x' + stram_id, 0)
            stram_id = f'********* {id} *********'
            print(stram_id)

            #print(frame_type)
            # 2. intercept the first http2 frame to be processed
            frame = s[:http_frame.frame_header_size + size]
            # 3. strip the frame to be processed
            s = s[http_frame.frame_header_size + size:]
            #print(s)
            if frame_type == http_frame.HTTP_HEADERS:
                print('Headers frame')
                self.hds.process(frame)
                #print(self.hds.tbl.print_tbl())
            elif frame_type == http_frame.HTTP_DATA:
                print('Data frame')
                self.dt.process(frame, self.hds.expect_grpc_data)
                #self.hds.expect_grpc_data = False
                self.dt.print_rst()
            elif frame_type == http_frame.SETTINGS:
                # to do
                print('Settings frame')
            else:
                print('FRAME TYPE: ' + str(frame_type))


	
