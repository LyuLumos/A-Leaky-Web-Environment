# bits = map(numberToBinary, range(256))
import base64
fileData = open('D:\GitHub\A-Leaky-Web-Environment\DiagonAlley\static\images\Marauders_Map_Scaled_large.png','rb')
all = fileData.readlines()

tail = all[-1]
# print(tail.find(bytes.fromhex('AE426082'))) # PNG 文件尾
string = tail[tail.find(bytes.fromhex('AE426082'))+4:]

print(base64.b32decode(string).decode('utf-8'))
