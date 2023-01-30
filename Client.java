import java.net.*;
import java.io.*;

public class Client {
    private static Socket clientSocket;
    private static PrintWriter out;
    private static BufferedReader in;
    
    public static void startConnection(String ip, int port) throws IOException{
        clientSocket = new Socket(ip, port);
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
    }

    public static String sendMessage(String msg) throws IOException {
        out.println(msg);
        out.flush();
        String resp = in.readLine();
        return resp;
    }

    public static void stopConnection() throws IOException{
        in.close();
        out.close();
        clientSocket.close();
    }

    public static void main(String[] args) throws IOException, InterruptedException{
        startConnection("localhost", 8080);
        System.out.println("Response: "+ sendMessage("Greetings"));

        while(true){
        long start = System.currentTimeMillis();
        System.out.println("Response: "+ sendMessage("changeColour,0,0,255"));
        long finish = System.currentTimeMillis();
        long timeElapsed = finish - start;
        System.out.println(timeElapsed);
        start = System.currentTimeMillis();
        System.out.println("Response: "+ sendMessage("changeColour,0,255,0"));
        finish = System.currentTimeMillis();
        timeElapsed = finish - start;
        System.out.println(timeElapsed);
        start = System.currentTimeMillis();
        System.out.println("Response: "+ sendMessage("changeColour,255,0,0"));
        finish = System.currentTimeMillis();
        timeElapsed = finish - start;
        System.out.println(timeElapsed);
    }
        
    }
        
    
}