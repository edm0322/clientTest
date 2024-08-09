import asyncio
import websockets
import json
import subprocess

SERVER_IP = "172.29.11.11:8000"

async def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

async def client():
    uri = "ws://" + SERVER_IP + "/ws/command/"  # 서버 주소를 적절히 변경하세요
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            if data['type'] == 'execute_command':
                command = data['command']
                print(f"Received command: {command}")
                
                result = await run_command(command)
                
                response = {
                    'type': 'client_command_result',
                    'command': command,
                    'result': result,
                    'client_id' : '172.29.22.22'
                }
                await websocket.send(json.dumps(response))

asyncio.get_event_loop().run_until_complete(client())
