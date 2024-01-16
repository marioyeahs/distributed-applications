import java.net.*;
import java.io.*;

class TalkToC {
   private String host = null;
   private int port = -999;
   private Socket socket = null;
   private BufferedReader inStream = null;

   public static void main(String[] args) {
      TalkToC caller = new TalkToC();
      caller.host = args[0];
      caller.port = Integer.valueOf(args[1]);
      caller.setUp();
      caller.converse();
      caller.cleanUp();
   }

   public void setUp() {
      System.out.println("TalkToC.setUp() invoked");

      try {
         socket = new Socket(host, port);
         inStream = new BufferedReader(new InputStreamReader(
         socket.getInputStream()));

         PrintWriter escritor = new PrintWriter(socket.getOutputStream(), true);

         BufferedReader lector = new BufferedReader(new InputStreamReader(socket.getInputStream()));
         System.out.println("Ingrese un número entero, si este es cero la comunicación se terminará:");
         BufferedReader teclado = new BufferedReader( new InputStreamReader(System.in));
         System.out.println("El eco del servidor dice:  " + teclado.readLine());
      } catch (UnknownHostException e) {
         System.err.println("Cannot find host called: " + host);
         e.printStackTrace();
         System.exit(-1);
      } catch (IOException e) {
         System.err.println("Could not establish connection for " + host);
         e.printStackTrace();
         System.exit(-1);
      }
   }

   public void converse() {
      System.out.println("TalkToC.converse() invoked");

      if (socket != null && inStream != null) {
         try {
            System.out.println(inStream.readLine());
         } catch (IOException e) {
            System.err.println("Conversation error with host " + host);
            e.printStackTrace();
         }
      }
   }

   public void cleanUp() {
      try {
         if (inStream != null)
            inStream.close();
         if (socket != null)
            socket.close();
      } catch (IOException e) {
         System.err.println("Error in cleanup");
         e.printStackTrace();
         System.exit(-1);
      }
   }
}