import paho.mqtt.client as mqtt 
import time
from hal import temperaturaEstufa1, aquecedor, rele
from definitions import user, password, client_id, server, port, tempIdeal

def mensagem (client, userdata, msg): #mudou o user porque o user do client.publish que precisamos não era esse que esta mais próximo. Receberíamos o user que estava sendo passado como parâmetro. Queremos o que vem de "definitions", o original, por isso mudamos o nome desse para userdata.
    vetor = msg.payload.decode().split(',') #cria um vetor com o parâmetro que é recebido do cayenne. O split serve para dividir o vetor em duas informações separadas por vírgula. 
    print(f'Temperatura atual da Estufa 1: {temp} graus Celcius.')
    rele('on' if vetor[1] == '1' and temp < tempIdeal else 'off')#se o vetor for 1 ele liga se não ele desliga 
    client.publish(f'v1/{user}/things/{client_id}/response', f'ok,{vetor [0]}') #confirma que o comando foi processado para o cayenne e para o botão
    #print (vetor)


# Conexão inicial
client = mqtt.Client(client_id)
client.username_pw_set(user, password)  
client.connect(server, port)

# Publish
client.on_message = mensagem #método que sera evocado quando receber uma mensagem do servidor 
client.subscribe (f'v1/{user}/things/{client_id}/cmd/1') #tópico que queremos do servidor 
client.loop_start() #serve para ficar monitorando o servidor 


# Comportamento do sistema 
while True:
    temp = temperaturaEstufa1()
    print(f'Temperatura atual da Estufa 1: {temp} graus Celcius.')
    client.publish('v1/'+user+'/things/'+client_id+'/data/0', 'temp,c=' + str(temp)) #mandando a mensagem de temperatura 
    time.sleep (5)

#client.disconnect()