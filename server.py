import requests
import asyncio
from pathlib import Path
import os



path1=(r'C:/Users/HP/Desktop/NET321_PRACTICUUM/net321/net322_25_cat2-main/net322_25_cat2-main/templates/index.html')
pathb=(r'C:/Users/HP/Desktop/NET321_PRACTICUUM/net321/net322_25_cat2-main/net322_25_cat2-main/templates/register.html')
file_s='db.txt'
async def client_handle(reader,writer):
    
    file_path=''
    username=''
    email=''
    response=''

    try:
    
        request= await reader.read(1020)
        request=request.decode()
        print(request)

        if not request:
             return

        lines=request.split('\r\n')
        request_line=request.splitlines()[0]
        method,path ,_=request_line.split()

        if method=="GET":
                if path=='/':
                        file_path=os.path.join(path1)

                elif path=='/register':
                        file_path=os.path.join(pathb)
            
                try:
                    with open(file_path,'r') as f:
                        content=f.read()  

                    response=f"HTTP/1.1 200 ok\r\nCotent-Type:  text/html\r\n\r\n{content}"   
                    writer.write(response.encode())
                    await writer.drain() 

                except Exception as e:
                      print("erro with the file: {e}")
                      response="HTTP /1.1 500 Internal Server Error\r\nContent-Type: text/plain \r\n\r\nServer Error"
                      writer.write(response.encode())
                      await writer .drain()
        
        elif method=="POST":
                body=request.split( '\r\n\r\n',1 )[-1]
                form={}
                for pair in  body.split('&'):
                    if '=' in pair:
                        key, value=pair.split('=',1)
                        form[key]=value
                username=form.get('username')
                email=form.get('email')


        if username and email:
                with open(file_s,'a') as f:
                        f.write(f"{username} {email}\n")
        renspone="HTTP/1.1 200 OK\r\nContetent-Type: text/plain\r\n\r\nREgistration successfull"
        writer.write(response.encode())
        await writer.drain()

    except Exception as e:
        print(f" Exeception: {e}")



async def main():
    port=8000
    address="127.0.0.1"
    server=await asyncio.start_server(client_handle,address,port) 
    print ("sever runing on:127.0.0.1 8000")

    async with server:
        await server.serve_forever()




if __name__ == "__main__":

   asyncio.run(main()) 