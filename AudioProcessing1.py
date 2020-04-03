import librosa
import os
import sounddevice
import soundfile
import sys
import queue
import threading

#Finding match file function
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name not in files:
            print("File does not exist!")
        
#Check for files availibility
check = input("Enter the text file name: ")
find(check, 'C:\Python Files\AudioProcessing1\Data\Raw')

file_dir = os.path.join('C:\Python Files\AudioProcessing1\Data\Raw', check)

#Splitting paragraph into sentences
text = open(file_dir, "r")
para = text.readlines()
extracted_sentence = []

for extract in para:
    sentence = extract.split('.')
    for s in sentence:
        s = s.strip()
        if s:
            extracted_sentence.append("\"" + s.strip() + ".\"")

print("{} sentences in the paragraph".format(len(extracted_sentence)))

#Output info
save = input("Enter folder name to save in: ")
if save == "ThoiSu":
    output_dir = "./Data/Output/ThoiSu"
elif save == "GocNhin":
    output_dir = "./Data/Output/GocNhin"
elif save == "TheGioi":
    output_dir = "./Data/Output/TheGioi"
elif save == "KinhDoanh":
    output_dir = "./Data/Output/KinhDoanh"
elif save == "GiaiTri":
    output_dir = "./Data/Output/GiaiTri"
elif save == "TheThao":
    output_dir = "./Data/Output/TheThao"
elif save == "PhapLuat":
    output_dir = "./Data/Output/PhapLuat"
elif save == "GiaoDuc":
    output_dir = "./Data/Output/GiaoDuc"
elif save == "SucKhoe":
    output_dir = "./Data/Output/SucKhoe"
elif save == "DoiSong":
    output_dir = "./Data/Output/DoiSong"
elif save == "DuLich":
    output_dir = "./Data/Output/DuLich"
elif save == "KhoaHoc":
    output_dir = "./Data/Output/KhoaHoc"
elif save == "SoHoa":
    output_dir = "./Data/Output/SoHoa"
elif save == "Xe":
    output_dir = "./Data/Output/Xe"
elif save == "YKien":
    output_dir = "./Data/Output/YKien"
elif save == "TamSu":
    output_dir = "./Data/Output/TamSu"
else:
    output_dir = "./Data/Output"
file_append = "sentence"

new_append = input("Enter audio file name: ")

if new_append:
    file_append = new_append

#Command stop recording
stop_cmd = "/s"

input_queue = queue.Queue()

def read_kb_input(input_queue):
    while True:
        input_str = input()
        input_queue.put(input_str)

#Output file function
def write_output(file, sentence, file_name):
    file.write(file_name + "\n")
    file.write(sentence + "\n")

q= queue.Queue()

#This is called for each audio block from a separate thread
def callback(indata, frames, time, status):
    if status:
        print(status, file = sys.stderr)
    q.put(indata.copy())

#Create a new audio file and record
def record(file_name):
    try:
        with soundfile.SoundFile(file_name, mode = 'x', samplerate = 22050, channels = 2, subtype = "PCM_24") as file:
            with sounddevice.InputStream(samplerate = 22050, device = sounddevice.default.device, channels = 2, callback = callback):
                print("Press {} to stop recording".format(stop_cmd))
                while True:
                    file.write(q.get())
                    if(input_queue.qsize() > 0):
                        input_str = input_queue.get()
                        if(input_str == stop_cmd):
                            break
    except Exception as e:
        print (e)

#Main function
def main():
    input_thread = threading.Thread(target = read_kb_input, args = (input_queue,), daemon = True)
    input_thread.start()
    
    output_file = open(os.path.join(output_dir, "Output.txt"), "a")

    i = 1
    for s in extracted_sentence:
        print("\"{}.\"\n".format(s))
        file_name = output_dir + '/' + file_append + "{}".format(i) + ".wav"
        i += 1
        print("Audio file name: " + file_name)
        input("Press to start recording.")
        record(file_name)
        write_output(output_file, s, file_name)

    output_file.close()
    return

main()