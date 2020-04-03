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
output_dir = "./Data\Output"
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
    
    i = 1
    for s in extracted_sentence:
        print("\"{}.\"\n".format(s))
        file_name = output_dir + '/' + file_append + "{}".format(i) + ".wav"
        i += 1
        print("Audio file name: " + file_name)
        input("Press to start recording.")
        record(file_name)
    return

main()