
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <unistd.h>
#include <sys/time.h>

void main(int argc, char *argv[])
{
   int portNum = atoi(argv[1]);
   int server;
   int client;
   int address_len;
   int sendrc;
   int bndrc;
   char *greeting;
   struct sockaddr_in local_Address;
   address_len = sizeof(local_Address);

   memset(&local_Address, 0x00, sizeof(local_Address));
   local_Address.sin_family = AF_INET;
   local_Address.sin_port = htons(portNum);
   local_Address.sin_addr.s_addr = htonl(INADDR_ANY);

#pragma convert(819)
   greeting = "This is a message from the C socket server.";
#pragma convert(0)

   /*  allocate socket    */
   if ((server = socket(AF_INET, SOCK_STREAM, 0)) < 0)
   {
      printf("failure on socket allocation\n");
      perror(NULL);
      exit(-1);
   }

   /* do bind   */
   if ((bndrc = bind(server, (struct sockaddr *)&local_Address, address_len)) < 0)
   {
      printf("Bind failed\n");
      perror(NULL);
      exit(-1);
   }

   /* invoke listen   */
   listen(server, 1);

   /* wait for client request */
   if ((client = accept(server, (struct sockaddr *)NULL, 0)) < 0)
   {
      printf("accept failed\n");
      perror(NULL);
      exit(-1);
   }

   /* send greeting to client    */
   if ((sendrc = send(client, greeting, strlen(greeting), 0)) < 0)
   {
      printf("Send failed\n");
      perror(NULL);
      exit(-1);
   }

   close(client);
   close(server);
}